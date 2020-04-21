# -*- coding: utf-8 -*-
from enum import Enum


class TraceLineData:
    def __init__(self, trace_line_str: str):
        self.__parse(trace_line_str)

    def get_source_operators(self) -> list:
        return self.instruction.source_operator

    def is_changed_in_this_line(self, track_registers):
        if self.instruction.changed_register:
            if self.instruction.changed_register in track_registers:
                return True
        return False


class ArmInstruction:
    def __init__(self, str_op_code: str, str_changed_register: str):
        self.__raw_str_op_code = str_op_code
        self.__raw_str_changed_register = str_changed_register
        self.__parse()
        self.changed_register = None
        if str_changed_register:
            self.changed_register = Register(str_changed_register.split("=")[0],
                                             int(str_changed_register.split("=")[1], 16))
        ...

    def __parse(self):
        if self.__raw_str_op_code:
            op_code_list = []
            for item in self.__raw_str_op_code.split(" "):
                if item != "":
                    if item[-1] == ",":
                        item = item.replace(",", "")
                    op_code_list.append(item)
            self.mnemonic = op_code_list[0]
            if len(op_code_list) >= 2:
                self.dest_operator = Operator()(op_code_list[1])
                self.source_operator = [Operator()(x) for x in op_code_list[2:]]
            else:
                self.dest_operator = op_code_list[1]
                self.source_operator = [Operator()(x) for x in op_code_list[1]]
            print(self.mnemonic, self.dest_operator, self.source_operator)


class OperatorType(Enum):
    Register = 1
    Immediate = 2
    IndirectAddress = 3
    UnKnow = 0

    @staticmethod
    def parse(operator_str):
        operator_type = OperatorType.UnKnow
        if operator_str[0] == "[":
            operator_type = OperatorType.IndirectAddress
        elif operator_str[0] == "#":
            operator_type = OperatorType.Immediate
        elif operator_str[0] in ["R", "S"]:
            operator_type = OperatorType.Register
        return operator_type


class Operator:
    def __call__(self, str_value: str):
        operator_type = OperatorType.parse(str_value)
        if operator_type == OperatorType.Register:
            return RegisterOperator(str_value)
        elif operator_type == OperatorType.Immediate:
            return ImmediateOperator(str_value)
        elif operator_type == OperatorType.IndirectAddress:
            return IndirectAddressOperator(str_value)


class Register:
    def __init__(self, register_name, register_value=0x0):
        self.register_name = register_name
        self.register_value = register_value

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Register):
            if o.register_name == self.register_name:
                return True
        return False

    def __repr__(self):
        return self.register_name + "=" + self.register_value


class RegisterOperator:
    def __init__(self, str_value: str):
        self.type = OperatorType.Register
        self.value = Register(str_value)


class ImmediateOperator:
    def __init__(self, str_value):
        self.type = OperatorType.Immediate
        self.value = str_value


class IndirectAddressOperator:
    def __init__(self, str_value):
        self.type = OperatorType.IndirectAddress
        self.value = []

    def __parse_indirect_address(self, str_indirect_address):
        ...
        # if str_indirect_address[0] == "[" and str_indirect_address[-1] == "]":
        #     str_indirect_value: str = str_indirect_address[1:-2]
        #     temp_list = str_indirect_value.split(",")
        #     for item in temp_list:
        #         if item[0] == "#":
        #             self.value.append(Immediate(item))
        #         elif item[0] in ["R", "S"]:
        #             self.value.append(Register(item))
        #         else:
        #             self.value.append(UnKnowOperator(item))
