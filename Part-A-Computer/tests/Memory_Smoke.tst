// Local smoke script for Memory.hdl. Official Memory.tst/Memory.cmp are still required.
load Memory.hdl,
output-file Memory_Smoke.out,
output-list out%B1.16.1;

// Write 1234 to RAM[0], then read it back.
set address 0,
set in 1234,
set load 1,
eval,
set load 0,
eval,
output;
