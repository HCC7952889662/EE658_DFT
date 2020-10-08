# Executed in Python 3.6
import re
from Circuit_Struct import *

def verilog_parser(filename):
    Circuit = Ckt()
    ipt = open(filename)
    connection_info = []
    eff_line = ''

    for line in ipt:
        # eliminate comment first
        line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
        if line_syntax:
            line = line[:line.index('//')]

        # considering ';' issues
        if ';' not in line and 'endmodule' not in line:
            eff_line = eff_line + line.rstrip()
            continue
        line = eff_line + line.rstrip()
        eff_line = ''
        if line != "":
            # wire
            line_syntax = re.match(r'^[\s]*wire (.*,*);', line, re.IGNORECASE)
            if line_syntax:
                for n in line_syntax.group(1).replace(' ', '').replace('\t', '').split(','):
                    new_connect = connect('wire', n)
                    connection_info.append(new_connect)

            # PI
            line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
            if line_syntax:
                for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                    new_node = Node(n, 'ipt')
                    Circuit.add_PI(new_node)
                    #print(Circuit.PI)
                    new_connect = connect('ipt', n)
                    new_connect.input_node.append(new_node)
                    connection_info.append(new_connect)

            # PO
            line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
            if line_syntax:
                for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                    new_node = Node(n, 'opt')
                    Circuit.add_PO(new_node)
                    new_connect = connect('opt', n)
                    new_connect.output_node.append(new_node)
                    connection_info.append(new_connect)

            # Module or Gate
            line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
            if line_syntax:
                if line_syntax.group(1) == 'module':
                    Circuit.circuit_name = line_syntax.group(2).replace(' ', '')

                else:
                    gate_order = line_syntax.group(3).replace(' ', '').split(',')
                    new_node = Node(line_syntax.group(2), line_syntax.group(1))
                    Circuit.add_object(new_node)
                    #Default Output is 1, so the gate order is OIIIIIII...
                    for index in range(len(gate_order)):
                        for C in connection_info:
                            # Output
                            if index == 0:
                                if C.name == gate_order[index]:
                                    C.input_node.append(new_node)
                            # Input
                            else:
                                if C.name == gate_order[index]:
                                    C.output_node.append(new_node)
    ipt.close()

    # Dealing with the connection
    for c in connection_info:
        for i in c.input_node:
            for o in c.output_node:
                o.fan_in_node.append(i)
                i.fan_out_node.append(o)


    return Circuit

def levelization(circuit):
    rest_node = circuit.node_list[:]
    print(circuit.PI)
    print("**********************")
    for node in circuit.PI:
        node.level = 0
        rest_node.remove(node)

    while rest_node:
        new_rest = []                # the rest node which cannot be processed currently
        new_valid = rest_node[:]     # the node which can be processed currently
        for node in rest_node:
            for upnode in node.fan_in_node:
                if upnode.level == -1:
                    new_rest.append(node)
                    new_valid.remove(node)
                    break
        for node in new_valid:
            if node.gate_type in ['not', 'nand', 'and', 'nor', 'or', 'xor', 'xnor', 'buff']:
                max_level = -1
                for upnode in node.fan_in_node:
                    max_level = max(max_level, upnode.level)
                node.level = max_level + 1
            # if the node is PO, the level = its fan-in gate level
            elif node.gate_type == 'opt':
                node.level = node.fan_in_node[0].level
        rest_node = new_rest

    for node in circuit.node_list:
        print("Node: "+ node.name +",  level="+ str(node.level))

try:
    #circuit_lock('s298')
    ckt = verilog_parser('ckt/c17.v')
    ckt.pc()
    levelization(ckt)


except IOError:
    print("error in the code")