# -*- coding: utf-8 -*-


class TraceFileParser:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.file_line_count = 0
        self.now_file_block = None
        self.raw_file_lines = self.__read_file_lines()

    def __read_file_lines(self, begin=0, end=100000):
        with open(self.__file_path, "r") as fh:
            file_lines = fh.readlines()
            self.file_line_count = len(file_lines)
            if len(file_lines) <= end:
                return file_lines
            else:
                return file_lines[begin:end]

    def get_line(self, line: int):
        ...

