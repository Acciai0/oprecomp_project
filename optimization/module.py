#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import pandas

from optimization.n_search import search
from optimization.iteration import Iteration
from optimization.model import create_optimization_model, solve_model

from argsmanaging import args
import benchmarks
import training
import data_gen
import utils


def __log_iteration(it: Iteration, t):
    form = "$"
    source = "$b#FOUND$"
    if it.has_failed:
        form = "$yellow#"
        source = "$b#yellow#GENERATED$"

    utils.print_n("[OPT] Solution n. {:d} " + source + " in {:.3f}s:", it.iter_n, t)

    target_label = "target error (log10)"
    error_label = "calculated error (log10)"
    predicted_label = "predicted error (log10)"
    utils.print_n("[OPT] $blue#{}$  |  $green#{}  {}$", target_label, error_label, predicted_label)

    pr = numpy.float_power(10, -it.get_predicted_error_log())

    formatted = "{:.3e} ({:.3f})".format(args.error, -numpy.log10(args.error))
    target = (" " * (len(target_label) - len(formatted))) + formatted
    formatted = "{:.3e} ({:.3f})".format(it.get_error(), it.get_error_log())
    error = (" " * (len(error_label) - len(formatted))) + formatted
    formatted = "{:.3e} ({:.3f})".format(pr, it.get_predicted_error_log())
    predicted = (" " * (len(predicted_label) - len(formatted))) + formatted
    utils.print_n("[OPT] " + form + "{}  |  {}  {}$", target, error, predicted)

    state = "$blue#FEASIBLE$" if it.is_feasible else "$red#NOT FEASIBLE$"
    utils.print_n("[OPT] Solution n. {:d} $b#cyan#{}$ is {}", it.iter_n, it.config, state)
    print()


def __get_predictions(config, regr, classifier):
    conf_df = pandas.DataFrame.from_dict({'var_{}'.format(i): [config[i]] for i in range(len(config))})
    prediction_with_conf = regr.predict(conf_df)[0]
    class_pred_with_conf = classifier.predict(conf_df)[0]
    return prediction_with_conf[0], class_pred_with_conf


def __iterate(bm: benchmarks.Benchmark, mdl, regressor, classifier, previous: Iteration):
    utils.stop_w.start()

    opt_config, prediction, class_prediction = solve_model(mdl, bm)
    failed = False
    if opt_config is None:
        failed = True
        opt_config = numpy.random.randint(args.min_bits_number, args.max_bits_number, bm.vars_number)
        prediction, class_prediction = __get_predictions(opt_config, regressor, classifier)
        prediction = float(prediction)
        class_prediction = float(class_prediction)
        opt_config = opt_config.tolist()

    error = benchmarks.run_benchmark_with_config(bm, opt_config, args)
    it = Iteration(opt_config, error, prediction, class_prediction, previous, failed)

    _, t = utils.stop_w.stop()
    __log_iteration(it, t)
    return it


def build_and_run_model(bm: benchmarks.Benchmark, regressor, classifier, session: training.TrainingSession,
                        max_iterations=100, log=None):
    utils.stop_w.start()
    mdl = create_optimization_model(bm, regressor, classifier)
    _, t = utils.stop_w.stop()
    utils.print_n("\n[OPT] Created first draft of the opt model in {:.3f}s\n", t)

    it = __iterate(bm, mdl, regressor, classifier, None)
    current_attempt = 0
    while current_attempt < args.steps and it.iter_n <= max_iterations:
        utils.stop_w.start()
        examples = data_gen.infer_examples_for_retraining(bm, session, it)
        _, t = utils.stop_w.stop()
        utils.print_n("[OPT] Inferred $green#{}$ more examples in {:.3f}s", len(examples), t)

        utils.stop_w.start()
        session, r_stats, c_stats = data_gen.ml_refinement(bm, regressor, classifier, session, examples)
        _, t = utils.stop_w.stop()
        utils.print_n("[OPT] Retrained regressor (MAE $green#{:.3f}$) and classifier "
                      "(accuracy $green#{:.3f}%$) in {:.3f}s", r_stats['MAE'], c_stats['accuracy'] * 100, t)

        if log is not None:
            log.insert_iteration(it, r_stats, c_stats)

        utils.stop_w.start()
        mdl.end()
        mdl = create_optimization_model(bm, regressor, classifier, it)
        _, t = utils.stop_w.stop()
        utils.print_n("[OPT] Refined opt model in {:.3f}s\n", t)

        if args.manual_toggled:
            input("[Press any button for next iteration]\n")

        best, _ = it.best_config_and_error
        if best is not None:
            current_attempt += 1
            utils.print_n("[OPT] $b#cyan#Extra attempt {}$", current_attempt)

        it = __iterate(bm, mdl, regressor, classifier, it)

    best, _ = it.best_config_and_error

    best = search(bm, session, best, log, args.search_version)

    return best, it.iter_n - current_attempt
