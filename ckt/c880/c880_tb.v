`timescale 1ns/1ns
module c880_tb;
integer fi0,fo0,fi1,fo1,fi2,fo2,fi3,fo3,fi4,fo4,fi5,fo5;
integer statusI;
integer in_name;
reg in [0:59];
wire out [0:25];
reg clk;
integer i;

c880 u_c880 (.N1(in[0]),.N8(in[1]),.N13(in[2]),.N17(in[3]),.N26(in[4]),.N29(in[5]),.N36(in[6]),.N42(in[7]),.N51(in[8]),.N55(in[9]),.N59(in[10]),.N68(in[11]),.N72(in[12]),.N73(in[13]),.N74(in[14]),.N75(in[15]),.N80(in[16]),.N85(in[17]),.N86(in[18]),.N87(in[19]),.N88(in[20]),.N89(in[21]),.N90(in[22]),.N91(in[23]),.N96(in[24]),.N101(in[25]),.N106(in[26]),.N111(in[27]),.N116(in[28]),.N121(in[29]),.N126(in[30]),.N130(in[31]),.N135(in[32]),.N138(in[33]),.N143(in[34]),.N146(in[35]),.N149(in[36]),.N152(in[37]),.N153(in[38]),.N156(in[39]),.N159(in[40]),.N165(in[41]),.N171(in[42]),.N177(in[43]),.N183(in[44]),.N189(in[45]),.N195(in[46]),.N201(in[47]),.N207(in[48]),.N210(in[49]),.N219(in[50]),.N228(in[51]),.N237(in[52]),.N246(in[53]),.N255(in[54]),.N259(in[55]),.N260(in[56]),.N261(in[57]),.N267(in[58]),.N268(in[59]),.N388(out[0]),.N389(out[1]),.N390(out[2]),.N391(out[3]),.N418(out[4]),.N419(out[5]),.N420(out[6]),.N421(out[7]),.N422(out[8]),.N423(out[9]),.N446(out[10]),.N447(out[11]),.N448(out[12]),.N449(out[13]),.N450(out[14]),.N767(out[15]),.N768(out[16]),.N850(out[17]),.N863(out[18]),.N864(out[19]),.N865(out[20]),.N866(out[21]),.N874(out[22]),.N878(out[23]),.N879(out[24]),.N880(out[25]));
initial begin
	i = 0;
	//test pattern0
	fi0 = $fopen("./input/c880_t0.txt","r");
	fo0 = $fopen("./gold/c880_t0_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi0,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo0,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi0);
	$fclose(fo0);
	i = 0;
	//test pattern1
	fi1 = $fopen("./input/c880_t1.txt","r");
	fo1 = $fopen("./gold/c880_t1_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi1,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo1,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi1);
	$fclose(fo1);
	i = 0;
	//test pattern2
	fi2 = $fopen("./input/c880_t2.txt","r");
	fo2 = $fopen("./gold/c880_t2_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi2,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo2,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi2);
	$fclose(fo2);
	i = 0;
	//test pattern3
	fi3 = $fopen("./input/c880_t3.txt","r");
	fo3 = $fopen("./gold/c880_t3_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi3,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo3,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi3);
	$fclose(fo3);
	i = 0;
	//test pattern4
	fi4 = $fopen("./input/c880_t4.txt","r");
	fo4 = $fopen("./gold/c880_t4_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi4,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo4,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi4);
	$fclose(fo4);
	i = 0;
	//test pattern5
	fi5 = $fopen("./input/c880_t5.txt","r");
	fo5 = $fopen("./gold/c880_t5_out.txt","w");
	while (i<=59) begin
		statusI = $fscanf(fi5,"%d,%b\n",in_name,in[i]);
		$display("i=%0d,in=%b\n",in_name,in[i]);
		i = i + 1;
	end
	i = 0;
	#1
	$display("N388=%b,N389=%b,N390=%b,N391=%b,N418=%b,N419=%b,N420=%b,N421=%b,N422=%b,N423=%b,N446=%b,N447=%b,N448=%b,N449=%b,N450=%b,N767=%b,N768=%b,N850=%b,N863=%b,N864=%b,N865=%b,N866=%b,N874=%b,N878=%b,N879=%b,N880=%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fwrite(fo5,"388,%b\n389,%b\n390,%b\n391,%b\n418,%b\n419,%b\n420,%b\n421,%b\n422,%b\n423,%b\n446,%b\n447,%b\n448,%b\n449,%b\n450,%b\n767,%b\n768,%b\n850,%b\n863,%b\n864,%b\n865,%b\n866,%b\n874,%b\n878,%b\n879,%b\n880,%b\n",out[0],out[1],out[2],out[3],out[4],out[5],out[6],out[7],out[8],out[9],out[10],out[11],out[12],out[13],out[14],out[15],out[16],out[17],out[18],out[19],out[20],out[21],out[22],out[23],out[24],out[25]);
	$fclose(fi5);
	$fclose(fo5);
	$finish;
end
endmodule
