# Verification status

## Personalisation
- Student: Nikhlesh Rohilla
- University roll number: 2501730005
- Personal number: K = 05 (numeric value 5)
- K mod 3 = 2: duplicate-label warnings
- K mod 4 = 1: 32-pixel width, two 16-bit screen words per row
- Starting row = 5; height = 20 rows
- First screen word = 16384 + (32 × 5) = 16544

## Verified locally
- 12 Python assembler unit tests passed.
- 2 box-generator tests passed.
- Add, Max and Rect local assembler outputs matched their checked-in `.hack` files.
- Box.asm and Box.hack regenerated for K=5.
- Local teaching-emulator draw and erase checks passed.

## Still required before final submission
- Run official CPU, Memory and Computer HDL tests in the Nand2Tetris Hardware Simulator.
- Compare against the official Add, Max, Rect and Pong programs using the official assembler. The bundled Pong file is only a smoke test.
- Demonstrate Box.hack in the official CPU Emulator.
- Insert genuine screenshots of the official HDL tests, assembler comparison, and box visible/cleared states into this report.
- Complete the report's programming mistake and correction section with a real example from the student's work.
