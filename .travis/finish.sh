#!/bin/sh

set -eux

case "$TEST_MODE"
in
    coverage)
        # Python
        if [ -f .coverage ]; then mv .coverage .coverage.orig; fi # FIXME: useless?
        coverage combine

        # C
        # Find the coverage file (in distutils's build directory)
        OBJDIR=$(dirname "$(find . -name pytracer.gcno | head -n 1)")
        (cd reprozip/native && lcov --directory ../../$OBJDIR -c -o reprozip.lcov)

        curl -s -o ~/codecov https://codecov.io/bash
        bash ~/codecov -X gcov
        ;;
esac
