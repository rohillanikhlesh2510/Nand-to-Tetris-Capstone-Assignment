# Part A — Build the Hack Computer

## HDL files

- `CPU.hdl`: A/D registers, ALU control, memory write control and jump control.
- `Memory.hdl`: RAM16K, Screen and Keyboard memory map.
- `Computer.hdl`: ROM32K + CPU + Memory integration.

## Official verification

1. Open the official Nand2Tetris Hardware Simulator.
2. Set the working directory to this folder.
3. Run the official `CPU.tst` and `Memory.tst`.
4. Run the official Computer integration tests supplied by the course (commonly ComputerAdd, ComputerMax and ComputerRect).
5. Save original screenshots showing each test's actual successful completion in `tests/evidence/`.

The course `.tst` and `.cmp` files are not included in this repository. Obtain them from the official course distribution. Do not claim a test passed based only on visual inspection of HDL source.

## Built-in chips

This implementation uses standard built-in chips such as `ALU`, `ARegister`, `DRegister`, `PC`, `RAM16K`, `Screen`, `Keyboard`, `ROM32K`, and the required mux/demux chips. In the report, clearly identify any chip that was replaced by a built-in chip, as required by the assignment.
