from distutils.core import setup, Extension

_module = Extension('demo', sources=['demomodule.c'])

setup(name='demo',
      version='1.0',
      description='This is a demo package',
      ext_modules=[_module])
