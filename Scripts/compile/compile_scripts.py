"""
Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from Utilities.unpyc3_compiler import Unpyc3PythonCompiler


Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join('..', '..', 'Release', 'ControlMenu'),
    names_of_modules_include=('controlmenu', 'sims4controlmenu',),
    output_ts4script_name='controlmenu'
)


Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join('..', '..', 'Release', 'ControlMenuTests'),
    names_of_modules_include=('controlmenu_tests',),
    output_ts4script_name='controlmenu_tests'
)
