import circuit
import re

class Checker():
    def __init__(self):
        """ create a circuit and a modelsim simulation
        we have two types of inputs: "gate-level-circuit" and a "verilog"
        verilog can be anything, gate level, behavioral, etc. 
        But gate-level-circuit can only be gate-level ckt or gate-level verilog 
        For now we are only supporting ckt for gate-level-circuit
        It is possible that both are the same, if we have a gate-level-verilog
        Objective: 
        we want to simulate the gate-level-circuit  with methods in class Circuit 
            and compare the results with modelsim simulation of the verilog. 
        Tasks: 
        - Check if the PI/PO of the files are the same -- raise error if not match
        - etc. 
        """
    def check_PI_PO(self, fname_ckt, fname_verilog):
        '''
        from http://sportlab.usc.edu/~msabrishami/benchmarks.html
        between CKT-658 and verilog
        circuit: 1355 has different PI/PO pins
        circuit: 17, 432, 499, 880, 1908, 3540, 5315, 6288 has the same PI/PO pins 
        '''
        fr_ckt = open(fname_ckt, mode = 'r')
        fr_verilog = open(fname_verilog, mode = 'r')
        PI_ckt = []
        PO_ckt = []
        PI_verilog = []
        PO_verilog = []
        eff_line = ''
        for line in fr_ckt:
            line_split = line.split(' ')
            if line[0] == '1':
                PI_ckt.append(line_split[1])
            if line[0] == '3':
                PO_ckt.append(line_split[1])
        for line in fr_verilog:

            line_syntax = re.match(r'^.*//.*', line, re.IGNORECASE)
            if line_syntax:
                line = line[:line.index('//')]

            if ';' not in line and 'endmodule' not in line:
                eff_line = eff_line + line.rstrip()
                continue
            line = eff_line + line.rstrip()
            eff_line = ''
            if line != "":
                # PI
                line_syntax = re.match(r'^.*input ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                       PI_verilog.append(n.lstrip('N'))
                # PO
                line_syntax = re.match(r'^.*output ([a-z]+\s)*(.*,*).*;', line, re.IGNORECASE)
                if line_syntax:
                    for n in line_syntax.group(2).replace(' ', '').replace('\t', '').split(','):
                        PO_verilog.append(n.lstrip('N'))

        PI_ckt.sort()
        PI_verilog.sort() 
        PO_ckt.sort() 
        PO_verilog.sort()
        if PI_ckt == PI_verilog and PO_ckt == PO_verilog:
            print('ckt and verilog files are the same!')
        else:
            print('ckt and verilog files are not the same')

    def check_IO_golden(self, circuit, golden_io_filename):
        #we have golden_test() in circuit
        # compares the results of logic-sim of this circuit, 
        #  ... provided a golden input/output file
        infile = open(golden_io_filename, "r")
        lines = infile.readlines()
        PI_t_order  = [x[1:] for x in lines[0][8:].strip().split(',')]
        PO_t_order = [x[1:] for x in lines[1][8:].strip().split(',')]
        PI_num = [x.num for x in circuit.PI]
        print("Logic-Sim validation with {} patterns".format(int((len(lines)-2)/3)))
        if PI_t_order != PI_num:
            print("Error: PI node order does not match! ")
            return False
        for t in range(int((len(lines)-2)/3)):
            test_in  = [int(x) for x in lines[(t+1)*3].strip().split(',')]
            test_out = [int(x) for x in lines[(t+1)*3+1].strip().split(',')]
            circuit.logic_sim(test_in)
            logic_out = circuit.read_PO()
            for i in range(len(PO_t_order)):
                out_node = PO_t_order[i]
                out_node_golden = test_out[i]
                if out_node_golden != logic_out["out"+str(out_node)]:
                    print("Error: PO node order does not match! ")
                    return False
        print("Validation completed successfully - all correct")
        return True

try:
    check = Checker()
    check.check_PI_PO('c6288.ckt', 'c6288.v')
except TypeError:
    print('TypeError!')
