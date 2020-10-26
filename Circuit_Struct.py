import re
import random
from Node_Struct import *
class Circuit:
	def __init__(self, filename):
		self.circuit_name = None  # The circuit name
		self.node_list = {}  # The Dict storing all nodes
		self.PI = []  # Primary input
		self.PO = []  # Primary output
		# Circuit Initialization
		self.verilog_parser(filename)
		self.nodes_lev = []  # list of all nodes, ordered by level

	def __str__(self):
		res = ["Circuit name: " + self.circuit_name]
		res.append("#Nodes: " + str(len(self.node_list)))
		res.append("#PI: " + str(len(self.PI)))
		res.append("#PO: " + str(len(self.PO)))

		for node in self.node_list.values():
			res.append(str(node))
		return "\n".join(res)

	def __del__(self):
		pass

	def add_object(self, obj):
		self.node_list[obj.name] = obj


	def add_PI(self, obj):
		self.add_object(obj)
		self.PI.append(obj)

	def add_PO(self, obj):  # Add an object to the PO list
		self.add_object(obj)
		self.PO.append(obj)

	def verilog_parser(self, filename):
		ipt = open(filename)
		connection_info = {}
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
						connection_info[n] = {'unode':[], 'dnode':[]}

				# PI
				line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
				if line_syntax:
					for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
						new_node = Node(n, 'ipt')
						self.add_PI(new_node)
						connection_info[n] = {'unode': [], 'dnode': []}
						connection_info[n]['unode'].append(new_node)

				# PO
				line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
				if line_syntax:
					for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
						new_node = Node(n, 'opt')
						self.add_PO(new_node)
						connection_info[n] = {'unode':[], 'dnode':[]}
						connection_info[n]['dnode'].append(new_node)

				# Module or Gate
				line_syntax = re.match(r'\s*(.+?) (.+?)\s*\((.*)\s*\);$', line, re.IGNORECASE)
				if line_syntax:
					if line_syntax.group(1) == 'module':
						self.circuit_name = line_syntax.group(2).replace(' ', '')

					else:
						gate_order = line_syntax.group(3).replace(' ', '').split(',')
						if line_syntax.group(1) == 'buf':
							new_node = BUFF(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'not':
							new_node = NOT(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'nor':
							new_node = NOR(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'or':
							new_node = OR(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'and':
							new_node = AND(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'nand':
							new_node = NAND(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'xor':
							new_node = XOR(line_syntax.group(2), line_syntax.group(1))
						elif line_syntax.group(1) == 'xnor':
							new_node = XNOR(line_syntax.group(2), line_syntax.group(1))
						else:
							break
						self.add_object(new_node)
						#Default Output is 1, so the gate order is OIIIIIII...
						for index in range(len(gate_order)):
							# Output
							if index == 0:
								connection_info[gate_order[index]]['unode'].append(new_node)
							# Input
							else:
								connection_info[gate_order[index]]['dnode'].append(new_node)
		ipt.close()

		# Dealing with the connection
		for wire in connection_info.keys():
			for i in connection_info[wire]['unode']:
				for o in connection_info[wire]['dnode']:
					o.fan_in_node.append(i)
					i.fan_out_node.append(o)

	def pc(self):
		print('Circuit Name: ', self.circuit_name)
		print('Total PI:', len(self.PI))
		print('Total PO:', len(self.PO))
		print('Total Nodes:', len(self.node_list))
		print('#################### Node Information ####################')
		for obj in self.node_list.values():
			print(obj.name + '(' + obj.gate_type + ')')
			print('fan_in:', end= ' ')
			for fi in obj.fan_in_node:
				print(fi.name, end= ' ')
			print('\nfan_out:', end= ' ')
			for fo in obj.fan_out_node:
				print(fo.name, end= ' ')
			print('\n')

	def levelization(self):
		queue = self.PI
		while len(queue) != 0:
			# Step 1: Set all PI to lev0 and update the number_of_input_level_defined
			for node in queue:
				if node.gate_type == 'ipt':
					node.level = 0
				elif node.gate_type != 'opt':
					# find the max level of input nodes
					max_level = node.fan_in_node[0].level
					for n in node.fan_in_node:
						max_level = max(max_level, n.level)
					node.level = max_level + 1
				else:
					node.level = node.fan_in_node[0].level

				if len(node.fan_out_node) > 0:
					for dnode in node.fan_out_node:
						dnode.number_of_input_level_defined += 1
						if dnode.number_of_input_level_defined == len(dnode.fan_in_node):
							# if it is same, then put this ready node into the queue
							queue.append(dnode)
				queue.remove(node)

		self.nodes_lev = sorted(list(self.node_list.values()), key=lambda x: x.level)


	def lev_print(self,outputfilename):
		fw=open(outputfilename,mode='w')
		fw.write(self.circuit_name+"\n")
		fw.write("#PI: "+str(len(self.PI))+"\n")
		fw.write("#PO: "+str(len(self.PO))+"\n")
		fw.write("#Nodes: "+str(len(self.node_list))+"\n")
		fw.write("#Gates: "+str(len(self.node_list) - len(self.PI) - len(self.PO))+"\n")
		print('Circuit Name: '+str(self.circuit_name)+"\n")
		print('#################### Node Information ####################')
		for obj in self.node_list.values():
			print(obj.name + ' : ' + str(obj.level))
			fw.write(obj.name + ' ' + str(obj.level)+"\n")
		fw.close()

	def test_pattern_generator(self, number_of_testbench):
		#create single file with multiple input patterns
		dir = './' + self.circuit_name + '/input/'
		filename = self.circuit_name + '_single.txt'
		fw = open(dir + filename, mode='w')
		for pi in self.PI:
			if len(self.PI)-1==self.PI.index(pi):
				fw.write(pi.name.lstrip('N'))
			else:
				fw.write(pi.name.lstrip('N')+',')
		fw.write('\n')
		for i in range(number_of_testbench):
			for pi in self.PI:
				random_int=random.randint(0,2)
				if len(self.PI)-1==self.PI.index(pi):
					if random_int==2:
						fw.write('X')
					else:
						fw.write(str(random_int))
				else:
					if random_int==2:
						fw.write('X,')
					else:
						fw.write(str(random_int)+',')
			fw.write('\n')
		fw.close()

	def testbench_generator(self, number_of_testbench):
		self.test_pattern_generator(number_of_testbench)
		dir = './' + self.circuit_name + '/'
		fw = open(dir + str(self.circuit_name) + "_tb.v", mode='w')
		fw.write("`timescale 1ns/1ns" + "\n")
		fw.write('module ' + str(self.circuit_name) + "_tb;" + '\n')
		fw.write("integer fi, fo;\n")
		fw.write('integer statusI;\n')
		fw.write('integer in_name;\n')
		fw.write('reg in [0:' + str(len(self.PI)-1) + '];\n')
		fw.write('wire out [0:' + str(len(self.PO) - 1) + '];\n')
		fw.write('reg clk;\n')
		fw.write('\n')
		fw.write(str(self.circuit_name) + ' u_' + str(self.circuit_name) + ' (')
		in_index = 0
		for pi in self.PI:
			fw.write('.' + pi.name + '(in[' + str(in_index) + ']),')
			in_index += 1
		out_index = 0
		for po in self.PO:
			fw.write('.' + po.name + '(out[' + str(out_index) + '])')
			if out_index != len(self.PO)-1:
				fw.write(',')
				out_index += 1
			else:
				fw.write(');\n')

		fw.write('initial begin\n')
		fw.write('\tfi = $fopen("./input/' + str(self.circuit_name) + '_single.txt","r");\n')
		fw.write('\tstatusI = $fscanf(fi,"')
		for j in range(len(self.PI)):
			fw.write('%s')
			if j != len(self.PI) - 1:
				fw.write(',')
			else:
				fw.write('\\n",')
		for j in range(len(self.PI)):
			fw.write('in[' + str(j) + ']')
			if j != len(self.PI) - 1:
				fw.write(',')
			else:
				fw.write(');\n')
		fw.write('\t#1\n')

		fw.write('\tfo = $fopen("./gold/golden_' + str(self.circuit_name) + '.txt","w");\n')
		fw.write('\tfo = $fopen("./gold/golden_' + str(self.circuit_name) + '.txt","a");\n')
		fw.write('\t$fwrite(fo,"Inputs: ')
		in_index = 0
		for pi in self.PI:
			fw.write(pi.name)
			if in_index != len(self.PI) - 1:
				fw.write(',')
				in_index += 1
			else:
				fw.write('\\n");\n')
		fw.write('\t$fwrite(fo,"Outputs: ')
		out_index = 0
		for pi in self.PO:
			fw.write(pi.name)
			if out_index != len(self.PO) - 1:
				fw.write(',')
				out_index += 1
			else:
				fw.write('\\n");\n')
		for i in range(number_of_testbench):
			fw.write('\t//test pattern' + str(i) + '\n')
			fw.write('\tstatusI = $fscanf(fi,"')
			for j in range(len(self.PI)):
				fw.write('%b')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(self.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t#1\n')
			fw.write('\t$display("')
			for j in range(len(self.PI)):
				fw.write('%b')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(self.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t$display("')
			out_index = 0
			for po in self.PO:
				fw.write(po.name + '=%b')
				if out_index != len(self.PO) - 1:
					fw.write(',')
					out_index += 1
				else:
					fw.write('\\n",')
					for j in range(len(self.PO)):
						fw.write('out[' + str(j) + ']')
						if j != len(self.PO) - 1:
							fw.write(',')
							out_index += 1
						else:
							fw.write(');\n')
			fw.write('\t$fwrite(fo, "Test # = ' + str(i) + '\\n");\n')
			fw.write('\t$fwrite(fo,"')
			for j in range(len(self.PI)):
				fw.write('%b')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(self.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(self.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t$fwrite(fo,"')
			for j in range(len(self.PO)):
				fw.write('%b')
				if j != len(self.PO) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(self.PO)):
				fw.write('out[' + str(j) + ']')
				if j != len(self.PO) - 1:
					fw.write(',')
				else:
					fw.write(');\n')


		fw.write('\t$fclose(fi);\n')
		fw.write('\t$fclose(fo);\n')

		fw.write('\t$finish;\n')
		fw.write('end\n')
		fw.write('endmodule\n')
		fw.close()
		#create run.bat
		dir = './' + str(self.circuit_name) + '/'
		fw = open(dir + "run.sh", mode='w')
		fw.write('vsim -c -do do_'+str(self.circuit_name)+'.do\n')
		fw.close()
		#create run.do
		fw = open(dir + 'do_'+str(self.circuit_name)+'.do', mode='w')
		fw.write('vlib work\n')
		fw.write('vmap work work\n')
		fw.write('vlog -work work '+str(self.circuit_name)+'.v\n')
		fw.write('vlog -work work '+str(self.circuit_name)+'_tb.v\n')
		fw.write('onerror {resume}\n')
		fw.write('vsim -novopt work.'+str(self.circuit_name)+'_tb\n')
		fw.write('run -all\n')
		fw.close()

	#def simulation(self,inputfilename,outputfilename):
	def simulation(self,test_pattern_count):
		max_level=0
		for node in self.node_list.values():
			if node.level>max_level:
				max_level=node.level

		#phase2 read multiple input patterns in one single file

		ipt=open('./'+self.circuit_name+'/input/'+self.circuit_name+'_single.txt',mode='r')
		fw=open('./'+self.circuit_name+'/output/'+self.circuit_name+'_single_out.txt',mode='w')
		fw2=open('./'+self.circuit_name+'/output/'+self.circuit_name+'_single_out_gold.txt',mode='w')
		fw2.write('Inputs: ')
		for node in self.PI:
			if len(self.PI)-1==self.PI.index(node):
				fw2.write(node.name+'\n')
			else:
				fw2.write(node.name+",")
		fw2.write('Outputs: ')
		for node in self.PO:
			if len(self.PO)-1==self.PO.index(node):
				fw.write(node.name.lstrip("N")+'\n')
				fw2.write(node.name+'\n')
			else:
				fw.write(node.name.lstrip("N")+",")
				fw2.write(node.name+",")

		read_line=ipt.readline()
		for i in range(test_pattern_count):
			fw2.write('Test # = '+str(i)+'\n')
			for node in self.node_list.values():#reset
				node.value=""
			read_line=ipt.readline()
			fw2.write(read_line)
			read_line_split=read_line.split(",")
			index=0
			for node in self.PI:
				node.value=read_line_split[index].replace('\n','')
				#print(node.name+",val="+node.value)
				index=index+1
			level=1
			Done=0
			while(Done==0):
				for node in self.node_list.values():
					if node.level==level and node.gate_type!="opt":
						#print("---"+node.name+",val="+node.value)
						node.operation()
						#print("-----"+node.name+",val="+node.value)
				if max_level==level:
					Done=1
				level+=1
			for node in self.PO:
				for fin_node in node.fan_in_node:
					result=fin_node.value
				node.value=result

			for node in self.PO:
				if len(self.PO)-1==self.PO.index(node):
					fw.write(node.value+'\n')
					fw2.write(node.value+'\n')
				else:
					fw.write(node.value+",")
					fw2.write(node.value+",")
				#print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value),end='')
				print(str(node.name)+":"+str(node.value)+' ',end='')
			print('')
		ipt.close()
		fw.close()
		fw2.close()



