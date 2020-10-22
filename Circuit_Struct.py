import re
import random
from Node_Struct import *
class Circuit:
	def __init__(self, filename):
		self.circuit_name = None  # The circuit name
		self.node_list = []  # The list storing all nodes
		self.node_name_list = [] # Name Information
		self.PI = []  # Primary input
		self.PO = []  # Primary output
		# Circuit Initialization
		self.verilog_parser(filename)

	def __del__(self):
		pass

	def add_object(self, obj):
		self.node_list.append(obj)               # the memory location of node, point to the node
		self.node_name_list.append(obj.name)     # the name of node: N1,N2...

	def add_PI(self, obj):
		self.add_object(obj)
		self.PI.append(obj)

	def add_PO(self, obj):  # Add an object to the PO list
		self.add_object(obj)
		self.PO.append(obj)

	def verilog_parser(self, filename):
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
						self.add_PI(new_node)
						#print(self.PI)
						new_connect = connect('ipt', n)
						new_connect.input_node.append(new_node)
						connection_info.append(new_connect)

				# PO
				line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
				if line_syntax:
					for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
						new_node = Node(n, 'opt')
						self.add_PO(new_node)
						new_connect = connect('opt', n)
						new_connect.output_node.append(new_node)
						connection_info.append(new_connect)

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

	def pc(self):
		print('Circuit Name: ', self.circuit_name)
		print('Total PI:', len(self.PI))
		print('Total PO:', len(self.PO))
		print('Total Nodes:', len(self.node_list))
		print('#################### Node Information ####################')
		for obj in self.node_list:
			print(obj.name + '(' + obj.gate_type + ')')
			print('fan_in:', end= ' ')
			for fi in obj.fan_in_node:
				print(fi.name, end= ' ')
			print('\nfan_out:', end= ' ')
			for fo in obj.fan_out_node:
				print(fo.name, end= ' ')
			print('\n')

	def levelization(self, outputfilename):
		# Step 0: Prepare a queue storing the finished nodes
		queue = []
		# Step 1: Set all PI to lev0 and update the number_of_input_level_defined
		for node in self.PI:
			node.level = 0
			for dnode in node.fan_out_node:
				dnode.number_of_input_level_defined += 1
				# Step 2: Checking whether number_of_input_level_defined is the same as fin
				if dnode.number_of_input_level_defined == len(dnode.fan_in_node):
					# if it is the same, then put this ready node into the queue
					queue.append(dnode)

		if len(queue) != 0:
			self.lev_recursive_part(queue)

		self.lev_print(outputfilename)

	def lev_recursive_part(self, queue):
		# Step 3: Do the judgement of the level of nodes in queue
		for node in queue:
			if node.gate_type != 'opt':
				# find the max level of input nodes
				max_level = node.fan_in_node[0].level
				for n in node.fan_in_node:
					max_level = max(max_level, n.level)
				node.level = max_level + 1
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
			self.lev_recursive_part(queue)

	def lev_print(self,outputfilename):
		fw=open(outputfilename,mode='w')
		fw.write(self.circuit_name+"\n")
		fw.write("#PI: "+str(len(self.PI))+"\n")
		fw.write("#PO: "+str(len(self.PO))+"\n")
		fw.write("#Nodes: "+str(len(self.node_list))+"\n")
		fw.write("#Gates: "+str(len(self.node_list) - len(self.PI) - len(self.PO))+"\n")
		print('Circuit Name: '+str(self.circuit_name)+"\n")
		print('#################### Node Information ####################')
		for obj in self.node_list:
			print(obj.name + ' : ' + str(obj.level))
			fw.write(obj.name + ' ' + str(obj.level)+"\n")
		fw.close()

	def test_pattern_generator(self, index):
		dir = './' + self.circuit_name + '/input/'
		filename = self.circuit_name + '_t' + str(index) + '.txt'
		fw = open(dir + filename, mode='w')
		for pi in self.PI:
			#fw.write(pi.name[1:] + ',' + str(random.randint(0,1)) + '\n')
			
			random_int=random.randint(0,2)
			if random_int==2:
				fw.write(pi.name[1:] + ',X' + '\n')
			else:
				fw.write(pi.name[1:] + ',' + str(random_int) + '\n')
			
		fw.close()

	def testbench_generator(self, number_of_testbench):
		dir = './' + self.circuit_name + '/'
		fw = open(dir + str(self.circuit_name) + "_tb.v", mode='w')
		fw.write("`timescale 1ns/1ns" + "\n")
		fw.write('module ' + str(self.circuit_name) + "_tb;" + '\n')
		fw.write("integer ")
		for i in range(number_of_testbench):
			fw.write('fi' + str(i) + ',fo' + str(i))
			if i != number_of_testbench-1:
				fw.write(',')
			else:
				fw.write(';\n')

		fw.write('integer statusI;\n')
		fw.write('integer in_name;\n')
		fw.write('reg in [0:' + str(len(self.PI)-1) + '];\n')
		fw.write('wire out [0:' + str(len(self.PO) - 1) + '];\n')
		fw.write('reg clk;\n')
		fw.write('integer i;\n\n')
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
		for i in range(number_of_testbench):
			self.test_pattern_generator(i)
			fw.write('\ti = 0;\n')
			fw.write('\t//test pattern' + str(i) + '\n')
			fw.write('\tfi' + str(i) +' = $fopen("./input/' + str(self.circuit_name)+ '_t' + str(i) + '.txt","r");\n')
			fw.write('\tfo' + str(i) + ' = $fopen("./gold/' + str(self.circuit_name) + '_t' + str(i) + '_out.txt","w");\n')
			fw.write('\twhile (i<=' + str(len(self.PI)-1) + ') begin\n')
			fw.write('\t\tstatusI = $fscanf(fi' + str(i) + ',"%d,%b\\n",in_name,in[i]);\n')
			fw.write('\t\t$display("i=%0d,in=%b\\n",in_name,in[i]);\n')
			fw.write('\t\ti = i + 1;\n')
			fw.write('\tend\n')
			fw.write('\ti = 0;\n')
			fw.write('\t#1\n')
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
			fw.write('\t$fwrite(fo' + str(i) + ',"')
			out_index = 0
			for po in self.PO:
				fw.write(po.name[1:] + ',%b\\n')
				if out_index != len(self.PO) - 1:
					out_index += 1
				else:
					fw.write('",')
					for j in range(len(self.PO)):
						fw.write('out[' + str(j) + ']')
						if j != len(self.PO) - 1:
							fw.write(',')
							out_index += 1
						else:
							fw.write(');\n')

			fw.write('\t$fclose(fi' + str(i) + ');\n')
			fw.write('\t$fclose(fo' + str(i) + ');\n')

		fw.write('\t$finish;\n')
		fw.write('end\n')
		fw.write('endmodule\n')
		fw.close()
		#create run.bat
		dir = './' + str(self.circuit_name) + '/'
		fw = open(dir + "run.sh", mode='w')
		fw.write('vsim -do do_'+str(self.circuit_name)+'.do\n')
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
		#phase1 code
		for i in range(0,test_pattern_count):
			ipt=open('./'+self.circuit_name+'/input/'+self.circuit_name+'_t'+str(i)+'.txt',mode='r')
			fw=open('./'+self.circuit_name+'/output/'+self.circuit_name+'_t'+str(i)+'_out.txt',mode='w')
			for node in self.node_list:#reset
				#node.value=0
				node.value=""
			for line in ipt:
				line_split=line.split(",")
				for node in self.PI:
					if node.name==("N"+line_split[0]):
						#node.value=int(line_split[1])
						node.value=line_split[1][:-1]
						#print(str(line_split[0])+",val="+str(node.value))
			level=1
			max_level=0
			for node in self.node_list:
				if node.level>max_level:
					max_level=node.level
			Done=0
			while(Done==0):
				for node in self.node_list:
					if node.level==level and node.gate_type!="opt":
						#print("---"+node.name+",val="+node.value)
						node.operation()
						#print("-----"+node.name+",val="+node.value)
				if max_level==level:
					Done=1
				level+=1
			for node in self.node_list:
				#print("---"+node.name+",val="+node.value)
				if node.gate_type=="opt":
					for fin_node in node.fan_in_node:
						#result=int(fin_node.value)
						result=fin_node.value
					node.value=result
			for node in self.node_list:
				if node.gate_type=="opt":
					fw.write(node.name.lstrip("N")+","+str(node.value)+"\n")
					print(str(node.name)+" "+str(node.gate_type)+" "+str(node.value))
			ipt.close()
			fw.close()
		#phase2


class connect():
	def __init__(self,type, name):
		self.type = type ##{'wire':1, 'reg':2}
		self.name = name
		self.input_node  = [] ## this wire is the Input of nodes in this list
		self.output_node = [] ## this wire is the Output of nodes in this list


