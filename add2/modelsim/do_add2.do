vlib work
vmap work work
vlog -work work add2.v
vlog -work work add2_tb.v

onerror {resume}
vsim -novopt work.add2_tb
run -all