#from Circuit_Struct import *
from Parser import *
class Node:
    def __init__(self, name: str, type:str):
        self.name = name  # Node name
        # Gate Type: ipt, opt, not, nand, and, nor, or, xor, xnor, buff
        self.gate_type = type  # Indicate which logic gate type this node is
        self.fan_in_node = []  # The list of fan-in nodes
        self.fan_out_node = []  # The list of fan-out nodes
        self.value = None  # the output value of this gate
        self.level = -1    # the initial value (null) of the level
        self.number_of_input_level_defined = 0

    def __del__(self):
        pass


class BUFF(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        self.value = self.fan_in_node[0].value

class NOT(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        if self.fan_in_node[0].value == 1:
            self.value = 0
        else:
            self.value = 1

class NAND(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        self.value = 0
        for fin_node in self.fan_in_node:
            if int(fin_node.value) == 0:
                self.value = 1
                break;

class NOR(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        self.value = 1
        for fin_node in self.fan_in_node:
            if int(fin_node.value) == 1:
                self.value = 0
                break;


class AND(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        self.value = 1
        for fin_node in self.fan_in_node:
            if int(fin_node.value) == 0:
                self.value = 0
                break;

class OR(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        self.value = 0
        for fin_node in self.fan_in_node:
            if int(fin_node.value) == 1:
                self.value = 1
                break;

class XOR(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        count = 0
        for fin_node in self.fan_in_node:
            if fin_node.value == 1:
                count += 1
        if count % 2 == 1:
            self.value = 1
        else:
            self.value = 0

class XNOR(Node):
    def __init__(self, name: str, type: str):
        Node.__init__(self, name, type)

    def operation(self):
        count = 0
        for fin_node in self.fan_in_node:
            if fin_node.value == 1:
                count += 1
        if count % 2 == 1:
            self.value = 0
        else:
            self.value = 1