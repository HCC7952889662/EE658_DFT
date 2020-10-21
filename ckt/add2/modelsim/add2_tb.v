`timescale 1ns/1ns
module add2_tb.v;
integer fi0,fi0;
integer statusI;
integer in_name;
reg in [0:4];
wire out [0:2];
reg clk;
integer i;

add2 u_add2 (.N1(in[0]),.N2(in[1]),.N3(in[2]),.N4(in[3]),.N5(in[4]),.N50(in[5]),.N51(in[5]),.N52(in[5]));
initial begin
	i = 0;
	//test pattern0
	fi0 = $fopen("./input/add2_t0.txt","r");
	fo0 = $fopen("./output/add2_t0.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi0,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo0,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi0);
	$fclose(fo0);
end
endmodule
