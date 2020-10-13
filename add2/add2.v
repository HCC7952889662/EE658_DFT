// Verilog
// add2
// Ninputs 5
// Noutputs 2
// NtotalGates 23
// NAND2 10
// AND2 2
// OR2 2
// NOT1 4
// BUFF1 5

module add2 (N1,N2,N3,N4,N5,N50,N51,N52);

input N1,N2,N3,N4,N5;

output N50,N51,N52;

wire N6,N7,N8,N9,N10,N11,N12,N13,N14,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29,N30,N31,N32,N33,N34,N35,N36,N37,N38,N39,N40,N41,N42,N43,N44,N45,N46,N47,N48,N49,N50;

buf BUF_1 (N6,N1);
buf BUF_2 (N9,N2);
buf BUF_3 (N12,N3);
buf BUF_4 (N15,N4);
buf BUF_5 (N18,N5);
not NOT_1 (N21,N6);
not NOT_2 (N30,N26);
not NOT_3 (N46,N42);
not NOT_4 (N37,N34);
or OR_1 (N22,N9,N12);
or OR_2 (N38,N15,N18);
and AND_1 (N50,N29,N31);
and AND_2 (N51,N45,N47);
nand NAND_1 (N23,N9,N12);
nand NAND_2 (N39,N15,N18);
nand NAND_3 (N29,N21,N26);
nand NAND_4 (N26,N22,N23);
nand NAND_5 (N42,N38,N39);
nand NAND_6 (N31,N6,N30);
nand NAND_7 (N34,N31,N23);
nand NAND_8 (N47,N34,N46);
nand NAND_9 (N45,N37,N42);
nand NAND_10 (N52,N47,N39);

endmodule