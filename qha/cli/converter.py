#!/usr/bin/env python3

import argparse

import qha
from qha.input_maker import FromQEOutput
from qha.cli.program import QHAProgram

class QHAConverter(QHAProgram):
    def __init__(self):
        super().__init__()

    def init_parser(self, parser):
        super().init_parser(parser)
        parser.add_argument('inp_file_list')
        parser.add_argument('inp_static')
        parser.add_argument('inp_q_points')

    def run(self, namespace):
        namespace = self.parser.parse_args()

        inp_file_list = namespace.inp_file_list
        inp_static = namespace.inp_static
        inp_q_points = namespace.inp_q_points

        converter = FromQEOutput(inp_file_list, inp_static, inp_q_points)
        converter.read_file_list()
        converter.read_static()
        converter.read_q_points()
        converter.read_frequency_files()
        converter.write_to_file()
