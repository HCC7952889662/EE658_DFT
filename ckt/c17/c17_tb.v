`timescale 1ns/1ns
module c17_tb;
integer fi0,fo0,fi1,fo1,fi2,fo2,fi3,fo3,fi4,fo4;
integer statusI;
integer in_name;
reg in [0:4];
wire out [0:1];
reg clk;
integer i;

c17 u_c17 (.N1(in[0]),.N2(in[1]),.N3(in[2]),.N6(in[3]),.N7(in[4]),.N22(out[0]),.N23(out[1]));
initial begin
