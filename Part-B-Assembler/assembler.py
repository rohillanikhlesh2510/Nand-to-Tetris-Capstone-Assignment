#!/usr/bin/env python3
"""Two-pass assembler for the 16-bit Nand2Tetris Hack computer."""
from pathlib import Path
import argparse
import json
import re
import sys

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
PREDEFINED.update({f"R{i}": i for i in range(16)})

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}

SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblerError(Exception):
    """Raised when an assembly source file contains invalid syntax."""


def clean_lines(source):
    """Return (original_line_number, whitespace-free_code) pairs."""
    path = Path(source)
    cleaned = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        code = raw.split("//", 1)[0].strip()
        if code:
            cleaned.append((line_number, re.sub(r"\s+", "", code)))
    return cleaned


def _format_errors(errors):
    return "\n".join(f"Line {line}: {message}" for line, message in errors)


def assemble(source, k=0, symbols_path=None):
    """
    Assemble a .asm file.

    Pass 1 records label -> ROM-address mappings.
    Pass 2 emits 16-bit instructions and allocates variables from RAM[16].
    For K % 3 == 1, all syntax errors are collected with source line numbers.
    """
    if not isinstance(k, int) or not 0 <= k <= 99:
        raise AssemblerError("K must be an integer from 0 to 99")

    lines = clean_lines(source)
    symbols = dict(PREDEFINED)
    rom_address = 0
    warnings = []
    errors = []

    # PASS 1: resolve labels before translating instructions.
    for line_number, line in lines:
        if line.startswith("(") or line.endswith(")"):
            if not (line.startswith("(") and line.endswith(")")):
                errors.append((line_number, "malformed label declaration"))
                continue
            label = line[1:-1]
            if not SYMBOL_RE.fullmatch(label):
                errors.append((line_number, f"invalid label name: {label!r}"))
                continue
            if label in symbols:
                if label in PREDEFINED:
                    errors.append((line_number, f"label {label} conflicts with a predefined symbol"))
                else:
                    warnings.append(
                        f"Line {line_number}: duplicate label ({label}); first definition kept"
                    )
                continue
            symbols[label] = rom_address
        else:
            rom_address += 1

    # PASS 2: translate A- and C-instructions.
    machine_code = []
    next_variable_address = 16

    for line_number, line in lines:
        if line.startswith("(") and line.endswith(")"):
            continue
        if line.startswith("(") or line.endswith(")"):
            continue  # malformed labels have already been reported in pass 1

        try:
            if line.startswith("@"):
                symbol_or_number = line[1:]
                if not symbol_or_number:
                    raise AssemblerError("missing A-instruction value")

                if symbol_or_number.isdecimal():
                    value = int(symbol_or_number)
                else:
                    if not SYMBOL_RE.fullmatch(symbol_or_number):
                        raise AssemblerError("invalid A-instruction symbol")
                    if symbol_or_number not in symbols:
                        symbols[symbol_or_number] = next_variable_address
                        next_variable_address += 1
                    value = symbols[symbol_or_number]

                if not 0 <= value <= 32767:
                    raise AssemblerError("A-instruction value must be between 0 and 32767")
                machine_code.append(f"{value:016b}")
                continue

            # C-instruction grammar: dest=comp;jump (dest and jump are optional).
            if line.count("=") > 1 or line.count(";") > 1:
                raise AssemblerError("malformed C-instruction")

            dest = ""
            jump = ""
            comp = line
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            if comp not in COMP:
                raise AssemblerError(f"invalid computation: {comp!r}")
            if dest not in DEST:
                raise AssemblerError(f"invalid destination: {dest!r}")
            if jump not in JUMP:
                raise AssemblerError(f"invalid jump: {jump!r}")

            machine_code.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])

        except AssemblerError as exc:
            errors.append((line_number, str(exc)))

    # K % 3 == 1 is the required line-numbered error-reporting feature.
    if errors:
        if k % 3 == 1:
            raise AssemblerError(_format_errors(errors))
        line, message = errors[0]
        raise AssemblerError(f"Line {line}: {message}")

    if symbols_path is not None:
        symbol_file = Path(symbols_path)
        symbol_file.parent.mkdir(parents=True, exist_ok=True)
        ordered = sorted(symbols.items(), key=lambda item: (item[1], item[0]))
        symbol_file.write_text(
            "".join(f"{name}\t{address}\n" for name, address in ordered),
            encoding="utf-8",
        )

    return machine_code, warnings, symbols


def main():
    parser = argparse.ArgumentParser(
        description="Translate Hack assembly (.asm) into 16-bit machine code (.hack)."
    )
    parser.add_argument("source", help="input .asm file")
    parser.add_argument("-o", "--output", help="output .hack file (default: same name as source)")
    parser.add_argument("--k", type=int, help="personal K: last two digits of the university roll number")
    parser.add_argument(
        "--symbols",
        help="symbol-table output path (default: Part-B-Assembler/symbols.txt)",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    try:
        config = json.loads((project_dir / "config.json").read_text(encoding="utf-8"))
        k = args.k if args.k is not None else int(config.get("K", 0))
        output_path = Path(args.output) if args.output else Path(args.source).with_suffix(".hack")
        symbols_path = Path(args.symbols) if args.symbols else project_dir / "symbols.txt"

        words, warnings, _ = assemble(args.source, k=k, symbols_path=symbols_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(words) + "\n", encoding="utf-8")

        print(f"Success: wrote {len(words)} 16-bit instructions to {output_path}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        feature = (
            "save symbol table",
            "line-numbered invalid-instruction errors",
            "duplicate-label warnings",
        )[k % 3]
        print(f"K={k}; required additional feature: {feature}")
    except (AssemblerError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ASSEMBLY FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
