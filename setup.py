# coding: utf-8

# python setup.py build

from cx_Freeze import setup, Executable

executables = [Executable('new_interface_demo.py')]

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='demo_interface',
      version='0.0.2',
      description='My App!',
      executables=executables,
      options=options)