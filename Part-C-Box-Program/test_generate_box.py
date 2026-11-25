import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_box import generate


class BoxGeneratorTests(unittest.TestCase):
    def test_personalisation_for_all_valid_k_values(self):
        for k in range(100):
            with self.subTest(k=k):
                source = generate(k)
                words_per_row = (k % 4) + 1
                first_address = 16384 + 32 * k
                self.assertIn(f"// Personal K = {k}", source)
                self.assertIn(f"// Top row = {k}; height = 20 rows; width = {words_per_row * 16} pixels ({words_per_row} words).", source)
                self.assertIn(f"@{first_address}", source)
                self.assertIn(f"@{words_per_row}", source)

    def test_rejects_k_outside_two_digit_range(self):
        for k in (-1, 100):
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    generate(k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
