# Executed in Python 3.6
import re
from Circuit_Struct import *

def command():
    Done=0
    while(Done==0):
        command_input=input("Command>")
        command_input=command_input.lower()
        command_name=command_input.split(" ")
        if command_name[0]=="read":
            if len(command_name)>1:
                ckt=Circuit(command_name[1])
                #ckt.verilog_parser(command_name[1])
            else:
                print("Please enter an input file name!")
        elif command_name[0]=="pc":
            ckt.pc()
        elif command_name[0]=="help":
            print("READ input_filename - read in circuit file and create all data structures")
            print("PC - print circuit information")
            print("HELP - print this help information")
            print("QUIT - stop and exit")
            print("LEV output_filename - levelize the circuit")
            print("LOGICSIM input_filename output_filename - simulate the circuit")
        elif command_name[0]=="quit":
            Done=1
        elif command_name[0]=="lev":
            if len(command_name)>1:
                ckt.levelization(command_name[1])
            else:
                print("Please enter an output file name!")
        elif command_name[0]=="logicsim":
            if len(command_name)>2:
                simulation(ckt,command_name[1],command_name[2])
            else:
                print("Please enter an input_filename and an output_filename!")
        elif command_name[0] == 'check':
            if len(command_name) > 2:
                file_check(command_name[1], command_name[2])
            else:
                print("Please enter an input_filename and an output_filename!")
        elif command_name[0] == 'tb_gen':
            if len(command_name) > 1:
                ckt.testbench_generator(int(command_name[1]))
            else:
                print("Please enter how many test vectors you want to generate!")
        else:
            print("Command not found!")

def simulation(circuit,inputfilename,outputfilename):
    ipt=open(inputfilename,mode='r')
    fw=open(outputfilename,mode='w')
    for node in circuit.node_list:#reset
        node.value=0
    for line in ipt:
        line_split=line.split(",")
        for node in circuit.PI:
            if node.name==("N"+line_split[0]):
                node.value=int(line_split[1])
                #print(str(line_split[0])+",val="+str(node.value))
    level=1
    max_level=0
    for node in circuit.node_list:
        if node.level>max_level:
            max_level=node.level
    Done=0
    while(Done==0):
        for node in circuit.node_list:
            if node.level==level and node.gate_type!="opt":
                operation(node)
        if max_level==level:
            Done=1
        level+=1
    for node in circuit.node_list:
        if node.gate_type=="opt":
            for fin_node in node.fan_in_node:
                result=int(fin_node.value)
            node.value=result
    for node in circuit.node_list:
        if node.gate_type=="opt":
            fw.write(node.name.lstrip("N")+","+str(node.value)+"\n")
            print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value))
    ipt.close()
    fw.close()

def operation(node):
    result_and=1
    result_nand=0
    result_or=0
    result_nor=1
    count1=0
    result=0
    if node.gate_type=="buf":
        for fin_node in node.fan_in_node:
            result=int(fin_node.value)
        node.value=result
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

def file_check(file1,file2):
    origin_output_file = open(file1, "r+")
    # print('reading', new_output_file)
    new_output_file = open(file2, "r+")
    number_of_line = 1
    origin_line = origin_output_file.readline()
    new_line = new_output_file.readline()
    flag = 1
    if len(origin_line) == 0:
        print("original file is empty!")
        flag = 0
    if len(new_line) == 0:
        print("new file is empty!")
        flag = 0
    if origin_line is not None and new_line is not None:
        while origin_line:
            if origin_line != new_line:
                print('file different! different line is #', number_of_line)
                flag = 0

            else:
                flag = 1
            origin_line = origin_output_file.readline()
            new_line = new_output_file.readline()
            number_of_line += 1
    if flag == 1:
        print('result are the same')
    else:
        print("result are not same!")
    origin_output_file.close()
    new_output_file.close()

try:
    command()

except IOError:
    print("error in the code")
