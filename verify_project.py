#!/usr/bin/env python3
"""Run local software tests; official HDL verification still requires Nand2Tetris tools."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
ASSEMBLER_DIR = ROOT / "Part-B-Assembler"
PART_C = ROOT / "Part-C-Box-Program"
sys.path.insert(0, str(ASSEMBLER_DIR))
sys.path.insert(0, str(PART_C))

from assembler import assemble
from generate_box import generate
from emulator import HackMachine


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.discover(str(ASSEMBLER_DIR / "tests")))
    suite.addTests(loader.discover(str(PART_C), pattern="test_*.py"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    k = int(json.loads((ASSEMBLER_DIR / "config.json").read_text(encoding="utf-8"))["K"])
    with tempfile.TemporaryDirectory() as temp_dir:
        symbol_file = Path(temp_dir) / "symbols.txt"

        # Locally included samples are syntax/encoding checks; Pong.asm is a smoke test.
        for name in ("Add", "Max", "Rect", "Pong"):
            source = ASSEMBLER_DIR / "programs" / f"{name}.asm"
            words, warnings, symbols = assemble(source, k=k, symbols_path=symbol_file)
            assert all(len(word) == 16 and set(word) <= {"0", "1"} for word in words)
            if name in ("Add", "Max", "Rect"):
                checked_in = source.with_suffix(".hack").read_text(encoding="utf-8").splitlines()
                assert words == checked_in, f"{name}.hack differs from local assembler output"

        box_source = generate(k)
        (PART_C / "Box.asm").write_text(box_source, encoding="utf-8")
        box_words, _, _ = assemble(PART_C / "Box.asm", k=k, symbols_path=symbol_file)
        box_hack = PART_C / "Box.hack"
        box_hack.write_text("\n".join(box_words) + "\n", encoding="utf-8")

        machine = HackMachine([int(word, 2) for word in box_words])
        first_word = 16384 + 32 * k
        words_per_row = (k % 4) + 1

        machine.key = 65
        for _ in range(60000):
            machine.step()
        drawn = [machine.ram[first_word + row * 32 + word]
                 for row in range(20) for word in range(words_per_row)]
        assert all(value == 0xFFFF for value in drawn), "Box did not draw correctly"

        machine.key = 0
        for _ in range(60000):
            machine.step()
        erased = [machine.ram[first_word + row * 32 + word]
                  for row in range(20) for word in range(words_per_row)]
        assert all(value == 0 for value in erased), "Box did not erase correctly"

    print("\\nLOCAL VERIFICATION PASSED")
    print(f"K={k}; top row={k}; height=20; width={(k % 4 + 1) * 16}px")
    print("Assembler tests, generator tests, sample assembly, box draw and box erase passed.")
    print("Official HDL tests, official Pong comparison, CPU Emulator screenshots and final report evidence remain separate submission tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
