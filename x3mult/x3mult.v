// Verilog
// x3mult
// Ninputs 3
// Noutputs 3
// NtotalGates 18

module x3mult (N1,N2,N3,N38,N39,N40);

input N1,N2,N3;

output N38,N39,N40;

wire N4,N9,N12,N15,N18,N19,N20,N23,N27,N28,N31,N32,N35,N36,N37;


buf BUF_1 (N4, N1);
buf BUF_2 (N9, N2);
buf BUF_3 (N12, N3);
not INT_1 (N15, N4);
not INT_2 (N18, N9);
not INT_3 (N19, N12);
not INT_4 (N32, N28);
and AND2_1 (N20, N18, N12);
and AND2_2 (N23, N19, N9);
and AND2_3 (N27, N15, N20);
and AND2_4 (N31, N15, N23);
and AND2_5 (N35, N4, N32);
and AND2_6 (N37, N4, N36);
and AND2_7 (N39, N4, N28);
or OR2_1 (N28, N20, N23);
or OR2_2 (N36, N32, N23);
or OR2_3 (N40, N31, N35);
or OR2_4 (N38, N27, N37);

endmodule