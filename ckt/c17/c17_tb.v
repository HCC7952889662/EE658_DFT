`timescale 1ns/1ns
module c17_tb;
integer fi0,fo0;
integer statusI;
integer in_name;
reg in [0:4];
wire out [0:1];
reg clk;
integer i;

c17 u_c17 (.N1(in[0]),.N2(in[1]),.N3(in[2]),.N6(in[3]),.N7(in[4]),.N22(out[0]),.N23(out[1]));
initial begin
	i = 0;
	//test pattern0
	fi0 = $fopen("./input/c17_t0.txt","r");
	fo0 = $fopen("./gold/c17_t0_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi0,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo0,"22,%b\n23,%b\n",out[0],out[1]);
	$fclose(fi0);
	$fclose(fo0);
	$finish;
end
endmodule
