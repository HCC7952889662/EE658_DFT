# Executed in Python 3.6
import re
import copy
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
    # Step 0: Prepare a queue storing the finished nodes
    queue = []
    # Step 1: Set all PI to lev0 and update the number_of_input_level_defined
    for node in circuit.PI:
        node.level = 0
        for dnode in node.fan_out_node:
            dnode.number_of_input_level_defined += 1;
            # Step 2: Checking whether number_of_input_level_defined is the same as fin
            if dnode.number_of_input_level_defined == len(dnode.fan_in_node):
                # if it is the same, then put this ready node into the queue
                queue.append(dnode)

    if len(queue) != 0:
        lev_recursive_part(queue)

    circuit.lev_print()

def lev_recursive_part(queue):
    # Step 3: Do the judgement of the level of nodes in queue
    for node in queue:
        if node.gate_type != 'opt':
            # find the max level of input nodes
            max_level = node.fan_in_node[0].level
            for n in node.fan_in_node:
                max_level = max(max_level, n.level)
            node.level = max_level + 1;
        else:
            node.level = node.fan_in_node[0].level
        # Step 4: Repeat the Step2 and Do Queue Maintainence
        if len(node.fan_out_node) > 0:
            for dnode in node.fan_out_node:
                dnode.number_of_input_level_defined += 1
                if dnode.number_of_input_level_defined == len(dnode.fan_in_node):
                    # if it is same, then put this ready node into the queue
                    queue.append(dnode)
        queue.remove(node)


    if len(queue) != 0:
        lev_recursive_part(queue)


try:
    ckt = verilog_parser('ckt/c499.v')
    #ckt.pc()
    levelization(ckt)


except IOError:
    print("error in the code")