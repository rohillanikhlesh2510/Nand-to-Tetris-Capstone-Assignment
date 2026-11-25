// Local smoke script for CPU.hdl. Not a substitute for the official CPU.tst/CPU.cmp.
load CPU.hdl,
output-file CPU_Smoke.out,
output-list pc%D1.6.1 outM%B1.16.1 writeM%B1.1.1 addressM%D1.5.1;

// A-instruction: load A with 7.
set inM 0,
set instruction %B0000000000000111,
eval,
output;

// C-instruction: D=A (1110110000010000).
set instruction %B1110110000010000,
eval,
output;
