# -*- coding: utf-8 -*-
from unittest import TestCase

from ida_trace_analysis_helper.ida_trace_file_helper.TraceFileParser import TraceFileParser


class TestTraceFileParser(TestCase):
    def setUp(self) -> None:
        self.parse = TraceFileParser("trace_log_1.log")

    def test_get_line(self):
        line = self.parse.get_line(10)
        self.assertIsNotNone(line)
        print(line)
