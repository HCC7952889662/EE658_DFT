# Executed in Python 3.6
from Circuit_Struct import *
class Command:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def command(self):
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
                    ckt.simulation(command_name[1],command_name[2])
                else:
                    print("Please enter an input_filename and an output_filename!")
            elif command_name[0] == 'check':
                if len(command_name) > 2:
                    self.file_check(command_name[1], command_name[2])
                else:
                    print("Please enter an input_filename and an output_filename!")
            elif command_name[0] == 'tb_gen':
                if len(command_name) > 1:
                    ckt.testbench_generator(int(command_name[1]))
                else:
                    print("Please enter how many test vectors you want to generate!")
            else:
                print("Command not found!")

    def file_check(self,file1,file2):
        origin_output_file = open(file1, "r+")
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
