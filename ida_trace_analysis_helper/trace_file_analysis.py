# -*- coding: utf-8 -*-
import re

from big_file_cache.BigFileCache import BigFileCache


class TrackRegisterInfo:
    def __init__(self, register_name, line_index):
        self.register_name = register_name
        self.line_index_when_used = []
        self.line_index_when_used.append(line_index)

    def __str__(self):
        return "{} User Line:{}".format(self.register_name, self.line_index_when_used)


class TraceLineData:
    def __init__(self, data: str, index):
        self.changed_registers = []
        self.instruction = []
        self.__data = data.strip()
        self.__parse(data)
        self.__index = index

    def __str__(self):
        return "in line[{}]:{}".format(self.__index, self.__data)

    def __repr__(self):
        return str(self)

    def __parse(self, data: str):
        list_data = [x.strip() for x in data.split("\t")]
        if len(list_data) != 5:
            raise Exception("is not raw ida trace data")
        for item in list_data[2].split(" "):
            if item:
                self.instruction.append(item)
        if len(self.instruction) > 2:
            self.changed_registers.append(self.instruction[1].replace(",",""))
        changed_registers = list_data[3].split(" ")
        for changed_register in changed_registers:
            if changed_register:
                register_name = changed_register.split("=")[0]
                for recorded_register in self.changed_registers:
                    if register_name[1:] != recorded_register[1:]:
                        self.changed_registers.append(register_name)


    def get_source_operators(self):
        source_operators = []
        if len(self.instruction) > 2:
            for item in self.instruction[2:]:
                if item[0] == "R" or item[0] == "W":
                    source_operators.append(TrackRegisterInfo(item.replace(",", ""), self.__index))
                elif item[0] == "[":
                    registers = re.findall(r"[WRX][0-9]+", item)
                    for register in registers:
                        source_operators.append(TrackRegisterInfo(register, self.__index))
        return source_operators

    def changed_in_this_line(self, track_registers: list):
        for track_register in track_registers:
            for changed_register in self.changed_registers:
                if track_register.register_name[1:] == changed_register[1:]:
                    track_registers.remove(track_register)
                    return track_register


class TraceFileAnalysisHelper:
    def __init__(self, trace_file_path: str):
        self.trace_file_path = trace_file_path
        self.trace_file = BigFileCache(self.trace_file_path)
        self.track_registers = []

    def analysis_end_with_line(self, begin: int, end: int):
        begin_line_data = TraceLineData(self.trace_file.read_line(begin), begin)
        print(begin_line_data)
        self.__update_track_registers(begin_line_data)
        for index in range(begin - 1, end, -1):
            index_line_data = TraceLineData(self.trace_file.read_line(index), index)
            track_info = index_line_data.changed_in_this_line(self.track_registers)
            if track_info:
                print(index_line_data, track_info)
                self.__update_track_registers(index_line_data)
                # print([str(x) for x in self.track_registers])
        print(self.track_registers)

    def is_already_in_track(self, operator: TrackRegisterInfo) -> TrackRegisterInfo:
        for track_register in self.track_registers:
            if track_register.register_name[1:] == operator.register_name[1:]:
                return track_register

    def __update_track_registers(self, trace_line_data: TraceLineData):
        source_operators = trace_line_data.get_source_operators()
        for source_operator in source_operators:
            already_in_track = self.is_already_in_track(source_operator)
            if already_in_track:
                already_in_track.line_index_when_used.extend(source_operator.line_index_when_used)
            else:
                self.track_registers.append(source_operator)
        return self.track_registers


if __name__ == '__main__':
    test_file_path = "../tests/raw_trace_001.log"
    analysis_helper = TraceFileAnalysisHelper(test_file_path)
    analysis_helper.analysis_end_with_line(11152, 0)
