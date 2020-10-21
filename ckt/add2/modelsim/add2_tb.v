`timescale 1ns/1ns
module add2_tb.v;
integer fi0,fi0,fi1,fi1,fi2,fi2,fi3,fi3,fi4,fi4,fi5,fi5;
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
	i = 0;
	//test pattern1
	fi1 = $fopen("./input/add2_t1.txt","r");
	fo1 = $fopen("./output/add2_t1.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi1,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo1,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi1);
	$fclose(fo1);
	i = 0;
	//test pattern2
	fi2 = $fopen("./input/add2_t2.txt","r");
	fo2 = $fopen("./output/add2_t2.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi2,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo2,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi2);
	$fclose(fo2);
	i = 0;
	//test pattern3
	fi3 = $fopen("./input/add2_t3.txt","r");
	fo3 = $fopen("./output/add2_t3.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi3,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo3,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi3);
	$fclose(fo3);
	i = 0;
	//test pattern4
	fi4 = $fopen("./input/add2_t4.txt","r");
	fo4 = $fopen("./output/add2_t4.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi4,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo4,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi4);
	$fclose(fo4);
	i = 0;
	//test pattern5
	fi5 = $fopen("./input/add2_t5.txt","r");
	fo5 = $fopen("./output/add2_t5.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi5,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N50=%b,N51=%b,N52=%b\n",out[0],out[1],out[2]);
	$fwrite(fo5,"50=%b,51=%b,52=%b\n",out[0],out[1],out[2]);
	$fclose(fi5);
	$fclose(fo5);
end
endmodule
