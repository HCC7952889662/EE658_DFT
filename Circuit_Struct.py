class Node:
	def __init__(self, name: str, type:str):
		self.name = name  # Node name
		# Gate Type: ipt, opt, not, nand, and, nor, or, xor, xnor, buff
		self.gate_type = type  # Indicate which logic gate type this node is
		self.fan_in_node = []  # The list of fan-in nodes
		self.fan_out_node = []  # The list of fan-out nodes
		self.value = None  # the output value of this gate
		self.level = -1    # the initial value (null) of the level

	def __del__(self):
		pass
	def add_fan_in(self, x):
		self.fan_in_node.append(x)

	def add_fan_out(self, x):
		self.fan_out_node.append(x)

	def remove_fan_in(self, x):
		self.fan_in_node.remove(x)

	def remove_fan_out(self, x):
		self.fan_out_node.remove(x)


class Ckt:
	def __init__(self):
		self.circuit_name = None  # The circuit name
		self.node_list = []  # The list storing all nodes
		self.node_name_list = [] # Name Information
		self.PI = []  # Primary input
		self.PO = []  # Primary output
		self.PI_count = 0 # IPT numbers
		self.PO_count = 0 #PO numbers
		self.node_count = 0 # How many nodes in the circuit

	def __del__(self):
		pass

	def add_object(self, obj):
		self.node_list.append(obj)               # the memory location of node, point to the node
		self.node_name_list.append(obj.name)     # the name of node: N1,N2...
		self.node_count += 1


	def add_PI(self, obj):
		self.add_object(obj)
		self.PI_count += 1
		self.PI.append(obj)

	def add_PO(self, obj):  # Add an object to the PO list
		self.add_object(obj)
		self.PO_count += 1


	def remove_node_from_PI(self, obj):
		self.PI.remove(obj)

	def remove_node_from_PO(self, obj):
		self.PO.remove(obj)

	def pc(self):
		print('Circuit Name: ', self.circuit_name)
		print('Total PI:', self.PI_count)
		print('Total PO:', self.PO_count)
		print('Total Nodes:', self.node_count)
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

class connect():
	def __init__(self,type, name):
		self.type = type ##{'wire':1, 'reg':2}
		self.name = name
		self.input_node  = [] ## this wire is the Input of nodes in this list
		self.output_node = [] ## this wire is the Output of nodes in this list