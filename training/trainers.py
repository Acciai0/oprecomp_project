#!/usr/bin/env python
# -*- coding: utf-8 -*-

import decimal

import numpy
import pandas
from sklearn import preprocessing, metrics, tree
import keras
from keras import models, layers, callbacks

from argsmanaging import args, Regressor, Classifier
import benchmarks
from training.session import TrainingSession


class RegressorTrainer:
    """
        Base class for trainers
    """

    learning_rate = .001

    NN_regressor_type = '_regrNN_2x1x'

    @staticmethod
    def create_for(regressor_type: Regressor, session: TrainingSession):
        if Regressor.NEURAL_NETWORK == regressor_type:
            return NNRegressorTrainer(session)
        return None

    def __init__(self, session: TrainingSession):
        self._session = session

    def create_regressor(self, bm: benchmarks.Benchmark):
        pass

    def train_regressor(self, regressor, epochs: int = 100, batch_size: int = 32, verbose=True, weights=None):
        pass

    def test_regressor(self, bm: benchmarks.Benchmark, regressor):
        pass


class NNRegressorTrainer(RegressorTrainer):
    def __init__(self, session: TrainingSession):
        super(NNRegressorTrainer, self).__init__(session)
        scaler = preprocessing.MinMaxScaler()
        self.__train_data_tensor = scaler.fit_transform(session.training_set)
        self.__test_data_tensor = scaler.fit_transform(session.test_set)
        self.__train_target_tensor = scaler.fit_transform(session.regressor_target.values.reshape(-1, 1))
        self.__test_target_tensor = scaler.fit_transform(session.regressor_target_test.values.reshape(-1, 1))

    def create_regressor(self, benchmark: benchmarks.Benchmark):
        n_samples, n_features = self.__train_data_tensor.shape
        input_shape = (self.__train_data_tensor.shape[1],)

        prediction_model = models.Sequential()

        if benchmark.is_flagged:
            prediction_model.add(layers.Dense(int(n_features / 2), activation='relu', input_shape=input_shape))
            prediction_model.add(layers.Dense(int(n_features / 4), activation='relu'))
            prediction_model.add(layers.Dense(n_features, activation='relu'))
        elif RegressorTrainer.NN_regressor_type == '_regrNN_2x1x':
            prediction_model.add(layers.Dense(n_features * 2, activation='relu',
                                              activity_regularizer=keras.regularizers.l1(1e-5),
                                              input_shape=input_shape))
            prediction_model.add(layers.Dense(n_features, activation='relu'))

        prediction_model.add(layers.Dense(1, activation='linear'))
        adam = keras.optimizers.Adam(lr=RegressorTrainer.learning_rate)
        prediction_model.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])
        return prediction_model

    def train_regressor(self, regressor, epochs: int = 100, batch_size: int = 32, verbose=True, weights=None):
        early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=10, min_delta=1e-5)
        reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', patience=5, min_lr=1e-5, factor=0.2)
        if weights is None:
            weights = numpy.full(len(self.__train_data_tensor), 1)
        regressor.fit(self.__train_data_tensor, self.__train_target_tensor, sample_weight=weights, epochs=epochs,
                      batch_size=batch_size, shuffle=True, validation_split=0.0, verbose=verbose,
                      callbacks=[early_stopping, reduce_lr])

    def test_regressor(self, bm: benchmarks.Benchmark, regressor):
        test_loss = regressor.evaluate(self.__test_data_tensor, self.__test_target_tensor, verbose=0)
        predicted = regressor.predict(self.__test_data_tensor)
        stats_res = {}
        pred_n_rows, pred_n_cols = predicted.shape
        pred = predicted[:, 0]
        if pred_n_cols > 1:
            mus = predicted[:, 0]
            predicted = mus
        else:
            predicted = pred

        abs_errors = []
        p_abs_errors = []
        sp_abs_errors = []
        squared_errors = []
        underest_count = 0
        overest_count = 0
        errors = []

        for i in range(len(predicted)):
            abs_errors.append(abs(predicted[i] - self.__test_target_tensor[i]))
            errors.append(predicted[i] - self.__test_target_tensor[i])
            squared_errors.append((predicted[i] - self.__test_target_tensor[i]) *
                                  (predicted[i] - self.__test_target_tensor[i]))
            if self.__test_target_tensor[i] != 0:
                p_abs_errors.append((abs(predicted[i] - self.__test_target_tensor[i])) *
                                    100 / abs(self.__test_target_tensor[i]))
            sp_abs_errors.append((abs(predicted[i] - self.__test_target_tensor[i])) * 100 /
                                 abs(predicted[i] + self.__test_target_tensor[i]))
            if predicted[i] - self.__test_target_tensor[i] > 0:
                overest_count += 1
            elif predicted[i] - self.__test_target_tensor[i] < 0:
                underest_count += 1

        stats_res["MAE"] = decimal.Decimal(numpy.mean(numpy.asarray(abs_errors)))
        stats_res["MSE"] = decimal.Decimal(numpy.mean(numpy.asarray(squared_errors)))
        stats_res["RMSE"] = decimal.Decimal(numpy.sqrt(stats_res["MSE"]))
        stats_res["MAPE"] = decimal.Decimal(numpy.mean(numpy.asarray(p_abs_errors)))
        stats_res["SMAPE"] = decimal.Decimal(numpy.mean(numpy.asarray(sp_abs_errors)))
        stats_res["ERRORS"] = errors
        stats_res["ABS_ERRORS"] = abs_errors
        stats_res["P_ABS_ERRORS"] = p_abs_errors
        stats_res["SP_ABS_ERRORS"] = sp_abs_errors
        stats_res["SQUARED_ERRORS"] = squared_errors
        stats_res["R2"] = metrics.r2_score(self.__test_target_tensor, predicted)
        stats_res["MedAE"] = metrics.median_absolute_error(self.__test_target_tensor, predicted)
        stats_res["EV"] = metrics.explained_variance_score(self.__test_target_tensor, predicted)
        stats_res["abs_errs"] = abs_errors
        stats_res["p_abs_errs"] = p_abs_errors
        stats_res["sp_abs_errs"] = sp_abs_errors
        stats_res["squared_errs"] = squared_errors
        stats_res["accuracy"] = 100 - abs(stats_res["MAPE"])
        stats_res["underest_count"] = underest_count
        stats_res["overest_count"] = overest_count
        stats_res["underest_ratio"] = underest_count / len(predicted)
        stats_res["overest_ratio"] = overest_count / len(predicted)

        stats_res['test_loss'] = test_loss

        max_conf = [args.max_bits_number] * bm.vars_number
        max_conf_dict = {}
        for i in range(len(max_conf)):
            max_conf_dict['var_{}'.format(i)] = [max_conf[i]]
        max_conf_df = pandas.DataFrame.from_dict(max_conf_dict)
        stats_res['max_prediction_error'] = regressor.predict(max_conf_df)[0][0]

        return stats_res


class ClassifierTrainer:
    @staticmethod
    def create_for(classifier_type: Classifier, session: TrainingSession):
        if Classifier.DECISION_TREE == classifier_type:
            return DTClassifierTrainer(session)
        return None

    def __init__(self, session: TrainingSession):
        self._session = session

    def create_classifier(self, bm: benchmarks.Benchmark):
        pass

    def train_classifier(self, classifier, weights=None,  weight_large_errors=10):
        pass

    def test_classifier(self, bm: benchmarks.Benchmark, classifier):
        predicted = classifier.predict(self._session.test_set)
        pred_classes = [0] * len(predicted)
        for i in range(len(predicted)):
            if .5 <= predicted[i]:
                pred_classes[i] = 1

        precision_s, recall_s, fscore_s, xyz = metrics.precision_recall_fscore_support(
            self._session.classifier_target_test, pred_classes, average='binary', pos_label=0)
        precision_l, recall_l, fscore_l, xyz = metrics.precision_recall_fscore_support(
            self._session.classifier_target_test, pred_classes, average='binary', pos_label=1)
        precision_w, recall_w, fscore_w, xyz = metrics.precision_recall_fscore_support(
            self._session.classifier_target_test, pred_classes, average='weighted')

        stats_res = {
            'small_error_precision': precision_s,
            'small_error_recall': recall_s,
            'small_error_fscore': fscore_s,
            'large_error_precision': precision_l,
            'large_error_recall': recall_l,
            'large_error_fscore': fscore_l,
            'precision': precision_w,
            'recall': recall_w,
            'fscore': fscore_w,
            'accuracy': metrics.accuracy_score(self._session.classifier_target_test, predicted)
        }
        return stats_res


class DTClassifierTrainer(ClassifierTrainer):
    def __init__(self, session: TrainingSession):
        super(DTClassifierTrainer, self).__init__(session)

    def create_classifier(self, bm: benchmarks.Benchmark):
        return tree.DecisionTreeClassifier(max_depth=bm.vars_number + 5)

    def train_classifier(self, classifier, weights=None, weight_large_errors=10):
        classes = self._session.classifier_target.tolist()
        if weights is None:
            weights = [1] * len(classes)
        if weight_large_errors != 1:
            for i in range(len(classes)):
                if 1 == classes[i]:
                    weights[i] *= weight_large_errors
        classifier.fit(self._session.training_set, self._session.classifier_target, sample_weight=weights)