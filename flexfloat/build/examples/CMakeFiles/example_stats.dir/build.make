# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/alberto/oprecomp/flexfloat

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/alberto/oprecomp/flexfloat/build

# Include any dependencies generated for this target.
include examples/CMakeFiles/example_stats.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/example_stats.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/example_stats.dir/flags.make

examples/CMakeFiles/example_stats.dir/example_stats.c.o: examples/CMakeFiles/example_stats.dir/flags.make
examples/CMakeFiles/example_stats.dir/example_stats.c.o: ../examples/example_stats.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alberto/oprecomp/flexfloat/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object examples/CMakeFiles/example_stats.dir/example_stats.c.o"
	cd /home/alberto/oprecomp/flexfloat/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/example_stats.dir/example_stats.c.o   -c /home/alberto/oprecomp/flexfloat/examples/example_stats.c

examples/CMakeFiles/example_stats.dir/example_stats.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/example_stats.dir/example_stats.c.i"
	cd /home/alberto/oprecomp/flexfloat/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alberto/oprecomp/flexfloat/examples/example_stats.c > CMakeFiles/example_stats.dir/example_stats.c.i

examples/CMakeFiles/example_stats.dir/example_stats.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/example_stats.dir/example_stats.c.s"
	cd /home/alberto/oprecomp/flexfloat/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alberto/oprecomp/flexfloat/examples/example_stats.c -o CMakeFiles/example_stats.dir/example_stats.c.s

examples/CMakeFiles/example_stats.dir/example_stats.c.o.requires:

.PHONY : examples/CMakeFiles/example_stats.dir/example_stats.c.o.requires

examples/CMakeFiles/example_stats.dir/example_stats.c.o.provides: examples/CMakeFiles/example_stats.dir/example_stats.c.o.requires
	$(MAKE) -f examples/CMakeFiles/example_stats.dir/build.make examples/CMakeFiles/example_stats.dir/example_stats.c.o.provides.build
.PHONY : examples/CMakeFiles/example_stats.dir/example_stats.c.o.provides

examples/CMakeFiles/example_stats.dir/example_stats.c.o.provides.build: examples/CMakeFiles/example_stats.dir/example_stats.c.o


# Object files for target example_stats
example_stats_OBJECTS = \
"CMakeFiles/example_stats.dir/example_stats.c.o"

# External object files for target example_stats
example_stats_EXTERNAL_OBJECTS =

examples/example_stats: examples/CMakeFiles/example_stats.dir/example_stats.c.o
examples/example_stats: examples/CMakeFiles/example_stats.dir/build.make
examples/example_stats: libflexfloat.a
examples/example_stats: examples/CMakeFiles/example_stats.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/alberto/oprecomp/flexfloat/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable example_stats"
	cd /home/alberto/oprecomp/flexfloat/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/example_stats.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/example_stats.dir/build: examples/example_stats

.PHONY : examples/CMakeFiles/example_stats.dir/build

examples/CMakeFiles/example_stats.dir/requires: examples/CMakeFiles/example_stats.dir/example_stats.c.o.requires

.PHONY : examples/CMakeFiles/example_stats.dir/requires

examples/CMakeFiles/example_stats.dir/clean:
	cd /home/alberto/oprecomp/flexfloat/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/example_stats.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/example_stats.dir/clean

examples/CMakeFiles/example_stats.dir/depend:
	cd /home/alberto/oprecomp/flexfloat/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/alberto/oprecomp/flexfloat /home/alberto/oprecomp/flexfloat/examples /home/alberto/oprecomp/flexfloat/build /home/alberto/oprecomp/flexfloat/build/examples /home/alberto/oprecomp/flexfloat/build/examples/CMakeFiles/example_stats.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/example_stats.dir/depend

