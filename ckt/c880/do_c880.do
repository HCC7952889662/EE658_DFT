vlib work
vmap work work
vlog -work work c880.v
vlog -work work c880_tb.v

onerror {resume}
vsim -novopt work.c880_tb
run -all