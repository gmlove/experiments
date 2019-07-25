#define PY_SSIZE_T_CLEAN
#include <Python.h>


static PyObject *DemoError;


static PyObject *
demo_system(PyObject *self, PyObject *args)
{
    const char *command;
    if (!PyArg_ParseTuple(args, "s", &command)){
        PyErr_SetString(DemoError, "no command input found");
        return NULL;
    }

    fprintf(stdout, "testing log in c, start executing command: %s\n", command);
    fflush(stdout);
    int sts = system(command);
    fprintf(stdout, "testing log in c, end executing command: %s\n", command);
    fflush(stdout);

    if (sts < 0) {
        PyErr_SetString(DemoError, "System command failed");
        return NULL;
    }

    return Py_True;
}


static PyObject *
demo_system_allow_thread(PyObject *self, PyObject *args)
{
    PyObject * ret;
    Py_BEGIN_ALLOW_THREADS
    ret = demo_system(self, args);
    Py_END_ALLOW_THREADS
    return ret;
}

static PyObject *
demo_heavy_calculation(PyObject *self, PyObject *args)
{
    fprintf(stdout, "testing log in c, start heavy calculation from\n");
    fflush(stdout);
    int a = 0;
    for (int i = 0; i < 10000000; i++) {
        a += 1;
        if (i > 0 && i % 2000000 == 0) {
            fprintf(stdout, "calculating a: %d\n", a);
            fflush(stdout);
        }
    }
    fprintf(stdout, "testing log in c, end heavy calculation from\n");
    fflush(stdout);
    return PyLong_FromLong(a);
}


static PyObject *
demo_heavy_calculation_allow_thread(PyObject *self, PyObject *args)
{
    PyObject * ret;
    Py_BEGIN_ALLOW_THREADS
    ret = demo_heavy_calculation(self, args);
    Py_END_ALLOW_THREADS
    return ret;
}


static PyMethodDef DemoMethods[] = {
    {"system",  demo_system, METH_VARARGS, "Execute a shell command."},
    {"system_allow_thread",  demo_system_allow_thread, METH_VARARGS, "Execute a shell command with allow thread."},
    {"heavy_calculation",  demo_heavy_calculation, METH_VARARGS, "Execute some heavy calculation."},
    {"heavy_calculation_allow_thread",  demo_heavy_calculation_allow_thread, METH_VARARGS, "Execute some heavy calculation with allow thread."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef demomodule = {
    PyModuleDef_HEAD_INIT,
    "demo",     /* name of module */
    NULL,       /* module documentation, may be NULL */
    -1,         /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    DemoMethods
};


PyMODINIT_FUNC
PyInit_demo(void)
{
    PyObject *m;

    m = PyModule_Create(&demomodule);
    if (m == NULL)
        return NULL;

    DemoError = PyErr_NewException("demo.error", NULL, NULL);
    Py_INCREF(DemoError);
    PyModule_AddObject(m, "error", DemoError);
    return m;
}
