# Executed in Python 3.6
import re
from Circuit_Struct import *

def command():
    Done=0
    while(Done==0):
        command_input=input("Command>")
        #command_input="read c17.v"
        command_name=command_input.split(" ")
        if command_name[0]=="read":
            if len(command_name)>1:
                ckt=verilog_parser(command_name[1])
        elif command_name[0]=="pc":
            ckt.pc()
        elif command_name[0]=="help":
            print("READ filename - read in circuit file and create all data structures")
            print("PC - print circuit information")
            print("HELP - print this help information")
            print("QUIT - stop and exit")
            print("LEV - levelize the circuit")
            print("SIM filename- simulate the circuit")
        elif command_name[0]=="quit":
            Done=1
        elif command_name[0]=="lev":
            levelization(ckt)
        elif command_name[0]=="sim":
            if len(command_name)>1:
                simulation(ckt,command_name[1])
        else:
            print("Command not found!")

def simulation(circuit,filename):
    #ipt=open(filename)
    ipt=open("ckt6288_test_in.txt")
    #ipt=open("ckt17_test_in.txt")
    for node in circuit.node_list:#reset
        node.value=0
    for line in ipt:
        line_split=line.split(",")
        for node in circuit.PI:
            if node.name==("N"+line_split[0]):
                node.value=int(line_split[1])
    level=1
    max_level=0
    for node in circuit.node_list:
        if node.level>max_level:
            max_level=node.level
    #for node in circuit.node_list:
        #if node.gate_type=="opt":
            #print(str(node.name)+" "+str(node.value))
    Done=0
    while(Done==0):
        for node in circuit.node_list:
            if node.level==level and node.gate_type!="opt":
                operation(node)
            #if node.gate_type=="opt":
                #print(str(node.name)+" "+str(node.value)+"!!!!!")
        if max_level==level:
            Done=1
        level+=1
    for node in circuit.node_list:
        if node.gate_type=="opt":
            for fin_node in node.fan_in_node:
                result=int(fin_node.value)
            node.value=result
    #for node in circuit.node_list:
        #print(str(node.name)+" "+str(node.value))
    for node in circuit.node_list:
        if node.gate_type=="opt":
            print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value))
    #for node in circuit.node_list:
        #if node.level>122:
            #print(str(node.name)+" "+str(node.value))
            #for fin_node in node.fan_in_node:
                #print(str(fin_node.name)+" "+str(fin_node.value))
            #print("--------------------")


def operation(node):
    result_and=1
    result_nand=0
    result_or=0
    result_nor=1
    count1=0
    result=0
    #print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value)+"------")

    if node.gate_type=="buff":
        for fin_node in node.fan_in_node:
            result=int(fin_node.value)
            #print(str(fin_node.name)+" "+str(fin_node.value))
        node.value=result

        #print(str(node.name)+" "+str(node.value))
        #print("--------------------")
    elif node.gate_type=="not":
        for fin_node in node.fan_in_node:
            result=int(fin_node.value)
        if result==1:
            node.value= 0
        else:
            node.value=1
    elif node.gate_type=="and":
        for fin_node in node.fan_in_node:
            if int(fin_node.value)==0:
                result_and=0
        node.value= result_and
    elif node.gate_type=="nand":
        for fin_node in node.fan_in_node:
            if int(fin_node.value)==0:
                result_nand=1
        node.value= result_nand
    elif node.gate_type=="or":
        for fin_node in node.fan_in_node:
            if int(fin_node.value)==1:
                result_or=1
        node.value= result_or
    elif node.gate_type=="nor":
        for fin_node in node.fan_in_node:
            if int(fin_node.value)==1:
                result_nor=0
        node.value= result_nor
    elif node.gate_type=="xor" or "xnor":
        for fin_node in node.fan_in_node:
            if int(fin_node.value)==1:
                count1+=1
        if node.gate_type=="xor":
            if count1%2==1:
                node.value= 1
            else:
                node.value= 0
        else:
            if count1%2==1:
                node.value= 0
            else:
                node.value= 1
    #print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value)+"------------------------")

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
    command()
    
    #ckt = verilog_parser('ckt/c17.v')
    #ckt.pc() 
    #levelization(ckt)
    

except IOError:
    print("error in the code")