# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT sig53_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT sig53_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND sig53_python_files python_bindings.cc)

gr_pybind_make_oot(sig53 ../../.. gr::sig53 "${sig53_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET sig53_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:sig53_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/sig53/)

install(
    TARGETS sig53_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/sig53
    COMPONENT pythonapi)
