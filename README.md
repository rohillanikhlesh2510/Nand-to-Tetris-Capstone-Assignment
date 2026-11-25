# Hack Computer Capstone — Nand2Tetris

An individual capstone implementation organised into the three required parts:

- **Student:** Nikhlesh Rohilla (Roll No. 2501730005; K = 05).
- **Part A:** Hack CPU, Memory and Computer HDL.
- **Part B:** two-pass Python assembler with the K-dependent duplicate-label warning feature.
- **Part C:** generated keyboard-controlled rectangle program and an optional Python teaching emulator.

## Personal configuration

`Part-B-Assembler/config.json` currently contains `K = 5`. Confirm this is the last two digits of Nikhlesh Rohilla's university roll number (2501730005) before submission.

For this configuration:

- `K mod 3 = 2` → duplicate-label warnings.
- `K mod 4 = 1` → 2 words per row.
- Box width = **32 pixels**.
- Top row = **5**; height = **20 rows**.
- First screen address = `16384 + 32 × 5 = 16544`.

## Requirements

- Python 3.10 or newer.
- Official Nand2Tetris Software Suite for Hardware Simulator and CPU Emulator.
- Official course test scripts and reference programs for final hardware verification and exact assembler comparisons.

## Run local verification

From the repository root in PowerShell:

```powershell
python verify_project.py
```

This runs the Python assembler unit tests, assembles the locally included sample programs, regenerates the personalised box, and checks draw/erase behaviour in the included teaching emulator.

## Run individual parts

### Part A — Hardware

Open `Part-A-Computer/CPU.hdl`, `Memory.hdl`, and `Computer.hdl` in the official Hardware Simulator. Run the course-provided CPU, Memory and Computer test scripts. Save genuine passing screenshots in `Part-A-Computer/tests/evidence/`.

The official `.tst` and `.cmp` files are not bundled. Do not report Part A as passed until those tests have actually run successfully.

### Part B — Assembler

```powershell
cd Part-B-Assembler
python -m unittest discover -s tests -v
python assembler.py programs/Add.asm
python assembler.py programs/Max.asm
python assembler.py programs/Rect.asm
python assembler.py programs/Pong.asm
```

`programs/Pong.asm` is explicitly a **smoke test**, not the official Pong game. For the assignment's exact comparison requirement, use the official `Pong.asm` supplied with the course distribution and compare its generated `.hack` output against the official assembler.

### Part C — Box program

```powershell
cd Part-C-Box-Program
python generate_box.py
cd ..\Part-B-Assembler
python assembler.py ..\Part-C-Box-Program\Box.asm -o ..\Part-C-Box-Program\Box.hack
cd ..\Part-C-Box-Program
python emulator.py Box.hack
```

Hold a key while the emulator window is focused to draw the box; release it to erase. This optional Python emulator is useful for local logic checks, but it does **not** replace the required official Nand2Tetris CPU Emulator demonstration.

## Submission checklist

- [ ] Confirm the student's name, roll number and K in the report and configuration.
- [ ] Run and capture official CPU, Memory and Computer HDL tests.
- [ ] Compare Add, Max, Rect and the official Pong program against official assembler output.
- [ ] Demonstrate Box.hack in the official CPU Emulator with key press and release.
- [ ] Add genuine screenshots and complete the report's actual mistake/correction section.
- [ ] Practise explaining the HDL, assembler passes, screen memory and K-dependent feature in the viva.

## Evidence integrity

`VERIFICATION_STATUS.md` records what was tested locally and what still requires the official course tools. Screenshots and test results must be captured from real executions; this repository does not fabricate official pass evidence.
