"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from Utilities.unpyc3_compiler import Unpyc3PythonCompiler


Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join('..', '..', 'Release', 'Sims4ControlMenu'),
    names_of_modules_include=('sims4controlmenu',),
    output_ts4script_name='sims4controlmenu'
)


Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join('..', '..', 'Release', 'Sims4ControlMenuTests'),
    names_of_modules_include=('sims4controlmenu_tests',),
    output_ts4script_name='sims4controlmenu_tests'
)
