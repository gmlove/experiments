
python setup.py build \
    && mv build/lib.*/demo.*.pyd ./ && \
    python perf_test.py
