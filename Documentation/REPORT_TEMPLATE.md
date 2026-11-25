# Hack Computer Capstone Report

**Name:** ____________________  
**Roll number:** ____________________  
**Personal K (last two digits):** ______  
**K mod 3:** ______  
**Box dimensions:** 16 × ((K mod 4) + 1) pixels wide × 20 rows high  
**Top screen row:** K

## 1. Objective
The objective of this capstone is to build and test the Hack computer, implement a two-pass Hack assembler in Python, and write a Hack assembly program that displays a personalised black rectangle while a keyboard key is pressed.

## 2. Part A — Hardware implementation
Briefly explain CPU.hdl, Memory.hdl and Computer.hdl. Mention any lab chip replaced with a built-in chip.

**Evidence:** Insert genuine screenshots for CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst and ComputerRect.tst. Write Pass/Fail beside each.

## 3. Part B — Python assembler
Explain the two passes, predefined symbols, labels, variables starting at RAM address 16, A-instruction encoding and C-instruction encoding. State which K-dependent extra feature you implemented.

**Evidence:** Insert the Python test output, one successful assembly output, and a screenshot/snippet of symbols.txt. Compare output with the official assembler.

## 4. Part C — Personalised box
State the formula and calculate your actual dimensions:
- Top row = K = ______
- Height = 20 rows
- Words per row = (K mod 4) + 1 = ______
- Width = 16 × words per row = ______ pixels

Explain how the program checks the keyboard and writes -1 to draw and 0 to erase the screen memory words.

**Evidence:** Insert a screenshot of the visible box in the CPU Emulator (and optionally the included Python demo emulator).

## 5. One mistake I fixed
Describe one real mistake you encountered, its cause, how you corrected it, and how you verified the fix. Do not invent an error; use something you actually experienced.

## 6. Conclusion
Summarise what you learned about hardware integration, binary instructions, symbol resolution, memory-mapped I/O and screen drawing.


## 7. Final evidence audit (complete before submission)
- Confirm that the name and roll number on this report belong to the submitting student.
- Confirm that K equals the last two digits of that student's roll number.
- List the exact official test filenames and their actual outcomes.
- Attach original screenshots; do not use emulator mock-ups as Hardware Simulator evidence.
- State clearly which chips were built in earlier labs and which built-in chips were used.
