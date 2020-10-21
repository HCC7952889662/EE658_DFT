vlib work
vmap work work
vlog -work work c17.v
vlog -work work c17_tb.v

onerror {resume}
vsim -novopt work.c17_tb
run -all