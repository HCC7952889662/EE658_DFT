# Executed in Python 3.6
from Circuit_Struct import *
import os
class Command:
    def __init__(self):
        self.test_pattern_count = 0

    def __del__(self):
        pass

    def command(self):
        Done=0
        infile=open('command.txt',mode='r')
        while(Done==0):
            #command_input=input("Command>")

            command_input=infile.readline()[:-1]

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
                print("LOGICSIM - simulate the circuit")
                print("CHECK - check the output files of ModelSim and our simulator")
                print("TB_GEN number- generate test patterns and testbench for ModelSim")
            elif command_name[0]=="quit":
                Done=1
            elif command_name[0]=="lev":
                if len(command_name)>1:
                    ckt.levelization(command_name[1])
                else:
                    print("Please enter an output file name!")
            elif command_name[0]=="logicsim":
                #if len(command_name)>2:
                    #ckt.simulation(command_name[1],command_name[2])
                ckt.simulation(self.test_pattern_count)
                #else:
                    #print("Please enter an input_filename and an output_filename!")
            elif command_name[0] == 'check':
                #if len(command_name) > 2:
                    #self.file_check(command_name[1], command_name[2])
                #else:
                #    print("Please enter an input_filename and an output_filename!")
                input("Press Enter key to continue after you run the simulation in ModelSim!")
                self.file_check(ckt)
                break
            elif command_name[0] == 'tb_gen':
                if len(command_name) > 1:
                    ckt.testbench_generator(int(command_name[1]))
                    self.test_pattern_count=int(command_name[1])
                else:
                    print("Please enter how many test vectors you want to generate!")
            else:
                print("Command not found!")
        infile.close()

    #def file_check(self,file1,file2):
    def file_check(self,ckt):
        self.test_pattern_count=5
        for i in range(0,self.test_pattern_count):
            #print(str(i))
            origin_output_file = open('./ckt/'+ckt.circuit_name+'/output/'+ckt.circuit_name+'_t'+str(i)+'_out.txt', "r+")
            new_output_file = open('./ckt/'+ckt.circuit_name+'/gold/'+ckt.circuit_name+'_t'+str(i)+'_out.txt', "r+")
            number_of_line = 1
            origin_line = origin_output_file.readline()
            #print(origin_line)
            new_line = new_output_file.readline()
            #print(new_line)
            flag = 1
            if len(origin_line) == 0:
                print("original file is empty!")
                flag = 0
            if len(new_line) == 0:
                print("new file is empty!")
                flag = 0
            if origin_line is not None and new_line is not None:
                while origin_line:
                    if origin_line.lower() != new_line.lower():
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
