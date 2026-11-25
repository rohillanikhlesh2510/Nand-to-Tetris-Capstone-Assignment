# Part C — Personalised key-controlled box

## Generate and assemble

From the repository root in PowerShell:

```powershell
cd Part-C-Box-Program
python generate_box.py
cd ..\Part-B-Assembler
python assembler.py ..\Part-C-Box-Program\Box.asm -o ..\Part-C-Box-Program\Box.hack
```

The generator reads `K` from `Part-B-Assembler/config.json`. Confirm that K is the last two digits of the submitting student's roll number before generating.

## Run the optional Python teaching emulator

```powershell
cd ..\Part-C-Box-Program
python emulator.py Box.hack
```

Focus the emulator window, hold any key to draw the rectangle, and release the key to erase it. This emulator is a local learning aid and automated logic-test target. It does **not** replace the required official Nand2Tetris CPU Emulator demonstration.

## Geometry

- Top row: `K`
- Height: 20 rows
- Width: `16 × ((K mod 4) + 1)` pixels
- First screen word: `SCREEN + 32 × K`
- Words per row: `(K mod 4) + 1`

The program polls the keyboard memory-mapped address, writes `-1` to make each selected 16-pixel word black, and writes `0` to clear it.
