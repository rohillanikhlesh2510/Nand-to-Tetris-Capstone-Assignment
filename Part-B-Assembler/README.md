# Part B — Python Hack Assembler

`assembler.py` implements a two-pass assembler for the 16-bit Hack instruction set.

## Run on Windows PowerShell

From the repository root:

```powershell
cd Part-B-Assembler
python -m unittest discover -s tests -v
python assembler.py programs/Add.asm
python assembler.py programs/Max.asm
python assembler.py programs/Rect.asm
python assembler.py programs/Pong.asm
```

Each command creates a matching `.hack` file. `symbols.txt` records predefined symbols, labels and variables for inspection.

## Personal K and required extra feature

Set `K` in `config.json` to the last two digits of Nikhlesh Rohilla's university roll number (2501730005). You can override it for a single run with `--k 41`.

- `K mod 3 = 0`: save labels and variables with their addresses in `symbols.txt`.
- `K mod 3 = 1`: report invalid instructions with their original source line numbers.
- `K mod 3 = 2`: warn when a label is declared more than once.

For the current repository configuration, `K=05`, so the required feature is duplicate-label warnings.

## Two-pass method

1. **Pass 1:** strip comments and blank lines, validate label declarations, and record each label's ROM address. Labels do not consume ROM addresses.
2. **Pass 2:** translate A-instructions and C-instructions into 16-bit binary. Unresolved variables receive RAM addresses starting at 16.

## Official comparison requirement

The locally included `Pong.asm` is clearly marked as a small **smoke test**, not the official Nand2Tetris Pong game. For the assignment's exact comparison requirement, obtain the official Add, Max, Rect and Pong programs from the course distribution, assemble each with this program and the official assembler, and compare the `.hack` files byte-for-byte.

The local verification script checks the included programs' encoding shape. It does not claim that the smoke-test Pong file is the official Pong assignment.
