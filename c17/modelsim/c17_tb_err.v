`timescale 1ns/1ns
module c17_tb;

integer fi0,fo0;
integer statusI0,statusO0;
reg [1:7] in;
reg [1:7] out;
reg clk;
integer i;

c17 u_c17 (.N1(),.N2(),.N3(),.N6(),.N7(),.N22(),.N23());

initial begin
	clk = 0;
	fi0 = $fopen("./input/c17_t0.txt","r");
	fo0 = $fopen("./output/c17_t0_out.txt","w");
end
	
always@(posedge clk) begin
	if($feof(fi0))  begin
		$fclose(fi0);
		$fclose(fo0);
		$stop;
	end
	statusI0 = $fscanf(fi0,"%b,%b\n",i,in[i]);
	out[i] = 1'b1 + in[i];
	$display("i=%0d,in=%b,out=%b\n",i,in[i],out[i]);
	$fmonitor(fo0,"%0d,%b\n",i,out[i]);
	statusI0 = $fscanf(fi0,"%b,%b\n",i,in[i]);
	out[i] = 1'b1 + in[i];
	$display("i=%d,in=%b,out=%b\n",i,in[i],out[i]);
end	

always #1 clk = ~clk;

endmodule