"""
The Sims 4 Control Menu is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from Utilities.compiler import compile_module


compile_module(
    root='..\\..\\Release\\Sims4ControlMenu',
    mod_scripts_folder='..',
    include_folders=('sims4controlmenu',),
    mod_name='sims4controlmenu'
)


compile_module(
    root='..\\..\\Release\\Sims4ControlMenuTests',
    mod_scripts_folder='..',
    include_folders=('sims4controlmenu_tests',),
    mod_name='sims4controlmenu_tests'
)
