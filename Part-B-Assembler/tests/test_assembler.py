import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assembler import AssemblerError, COMP, DEST, JUMP, PREDEFINED, assemble


class AssemblerTests(unittest.TestCase):
    def assemble_text(self, text, k=70):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "case.asm"
            symbols = Path(directory) / "symbols.txt"
            source.write_text(text, encoding="utf-8")
            words, warnings, table = assemble(source, k=k, symbols_path=symbols)
            saved = symbols.read_text(encoding="utf-8")
            return words, warnings, table, saved

    def test_add_program_expected_machine_code(self):
        words, _, _, _ = self.assemble_text("@2\nD=A\n@3\nD=D+A\n@0\nM=D\n")
        self.assertEqual(words, [
            "0000000000000010",
            "1110110000010000",
            "0000000000000011",
            "1110000010010000",
            "0000000000000000",
            "1110001100001000",
        ])

    def test_forward_label_and_variable_allocation(self):
        words, _, symbols, _ = self.assemble_text(
            "@END\n@counter\nM=1\n(END)\n@counter\n0;JMP\n"
        )
        self.assertEqual(symbols["END"], 3)
        self.assertEqual(symbols["counter"], 16)
        self.assertEqual(words[0], "0000000000000011")
        self.assertEqual(words[1], "0000000000010000")

    def test_predefined_symbols(self):
        _, _, symbols, _ = self.assemble_text("@SP\n@R15\n@SCREEN\n@KBD\n")
        for name, address in PREDEFINED.items():
            self.assertEqual(symbols[name], address)

    def test_comments_and_whitespace(self):
        words, _, _, _ = self.assemble_text(
            "  // comment\n @2   // inline\n D = A \n\n"
        )
        self.assertEqual(words, ["0000000000000010", "1110110000010000"])

    def test_all_comp_dest_jump_encodings_are_16_bits(self):
        # Exercise the complete lookup tables and the C-instruction bit layout.
        for comp, comp_bits in COMP.items():
            for dest, dest_bits in DEST.items():
                for jump, jump_bits in JUMP.items():
                    with self.subTest(comp=comp, dest=dest, jump=jump):
                        source_line = (dest + "=" if dest else "") + comp + (";" + jump if jump else "")
                        words, _, _, _ = self.assemble_text(source_line)
                        self.assertEqual(words, ["111" + comp_bits + dest_bits + jump_bits])
                        self.assertEqual(len(words[0]), 16)

    def test_duplicate_label_warning(self):
        _, warnings, symbols, _ = self.assemble_text("(LOOP)\n@0\n(LOOP)\n@1\n", k=2)
        self.assertEqual(symbols["LOOP"], 0)
        self.assertTrue(any("duplicate label" in warning for warning in warnings))

    def test_k1_reports_original_line_numbers_and_multiple_errors(self):
        with self.assertRaises(AssemblerError) as caught:
            self.assemble_text("// heading\n@0\nD=BAD\n@1\nQ=M\n", k=70)
        message = str(caught.exception)
        self.assertIn("Line 3:", message)
        self.assertIn("Line 5:", message)

    def test_invalid_a_instruction_range(self):
        with self.assertRaisesRegex(AssemblerError, "32767"):
            self.assemble_text("@32768\n", k=70)

    def test_invalid_symbol_and_malformed_c_instruction(self):
        for text in ("@\n", "@bad-symbol\n", "D==A\n", "D=A;JMP;JGT\n"):
            with self.subTest(text=text):
                with self.assertRaises(AssemblerError):
                    self.assemble_text(text, k=70)

    def test_label_cannot_override_predefined_symbol(self):
        with self.assertRaisesRegex(AssemblerError, "predefined symbol"):
            self.assemble_text("(SCREEN)\n@SCREEN\n", k=70)

    def test_k_must_be_two_digits(self):
        with self.assertRaisesRegex(AssemblerError, "0 to 99"):
            self.assemble_text("@0\n", k=100)

    def test_symbol_file_contains_labels_and_variables(self):
        _, _, _, saved = self.assemble_text("(START)\n@variable\n0;JMP\n")
        self.assertIn("START\t0", saved)
        self.assertIn("variable\t16", saved)


if __name__ == "__main__":
    unittest.main(verbosity=2)
