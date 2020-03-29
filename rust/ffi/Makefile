c-build-linux:
	cd out_c && \
	gcc -shared -fPIC ../src_c/mul.cc -o libmul.so && \
	gcc -shared -fPIC ../src_c/double.cc -I../src_c/ -L. -lmul -o libdouble.so && \
	gcc ../src_c/main.c -o test_double -I../src_c/ -L. -ldouble -lmul

c-build-win:
	cd out_c && \
	cl /LD ../src_c/mul.cc && \
	cl /LD ../src_c/double.cc /link mul.lib && \
	cl /LD ../src_c/main.c /link double.lib && \

c-build-mac:
	cd out_c && \
	gcc -dynamiclib ../src_c/mul.cc -o libmul.dylib && \
	gcc -dynamiclib ../src_c/double.cc -I../src_c/ -L. -lmul -undefined suppress -flat_namespace -o libdouble.dylib && \
	gcc ../src_c/main.c -I../src_c/ -L. -lmul -ldouble -o test_double

c-test:
	cargo build --test c
	cd out_c/ && \
        ../target/debug/c-8c59e89f28cbe12b it_works --nocapture --exact
