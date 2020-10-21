`timescale 1ns/1ns
module c17_tb;

integer fi0,fo0,fi1,fo1,fi2,fo2,fi3,fo3,fi4,fo4,fi5,fo5;
integer statusI;
integer in_name;
reg in [0:4];
wire out [0:1];
reg clk;
integer i;

c17 u_c17 (.N1(in[0]),.N2(in[1]),.N3(in[2]),.N6(in[3]),.N7(in[4]),
           .N22(out[0]),.N23(out[1]));

initial begin
	i = 0;

	//test pattern0
	fi0 = $fopen("./input/c17_t0.txt","r");
	fo0 = $fopen("./output/c17_t0_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi0,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo0,"22,%b\n",out[0]);
	$fwrite(fo0,"23,%b\n",out[1]);
	$fclose(fi0);
	$fclose(fo0);
	
	//test pattern1
	fi1 = $fopen("./input/c17_t1.txt","r");
	fo1 = $fopen("./output/c17_t1_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi1,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo1,"22,%b\n",out[0]);
	$fwrite(fo1,"23,%b\n",out[1]);
	$fclose(fi1);
	$fclose(fo1);
	
	//test pattern2
	fi2 = $fopen("./input/c17_t2.txt","r");
	fo2 = $fopen("./output/c17_t2_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi2,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo2,"22,%b\n",out[0]);
	$fwrite(fo2,"23,%b\n",out[1]);
	$fclose(fi2);
	$fclose(fo2);
	
	//test pattern3
	fi3 = $fopen("./input/c17_t3.txt","r");
	fo3 = $fopen("./output/c17_t3_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi3,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo3,"22,%b\n",out[0]);
	$fwrite(fo3,"23,%b\n",out[1]);
	$fclose(fi3);
	$fclose(fo3);
	
	//test pattern4
	fi4 = $fopen("./input/c17_t4.txt","r");
	fo4 = $fopen("./output/c17_t4_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi4,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo4,"22,%b\n",out[0]);
	$fwrite(fo4,"23,%b\n",out[1]);
	$fclose(fi4);
	$fclose(fo4);
	
	//test pattern5
	fi5 = $fopen("./input/c17_t5.txt","r");
	fo5 = $fopen("./output/c17_t5_out.txt","w");
	while (i<=4) begin
		statusI = $fscanf(fi5,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N22=%b,N23=%b\n",out[0],out[1]);
	$fwrite(fo5,"22,%b\n",out[0]);
	$fwrite(fo5,"23,%b\n",out[1]);
	$fclose(fi5);
	$fclose(fo5);

	$stop;	
end

endmodule