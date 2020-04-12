# -*- coding: utf-8 -*-
from unittest import TestCase

from ida_trace_analysis_helper.utils.big_file_cache import BigFileCache


class TestBigFileCache(TestCase):
    def setUp(self) -> None:
        self.file = BigFileCache("trace_log_1.log")


