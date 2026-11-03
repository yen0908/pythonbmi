import unittest

from domain.bmi import calculate_bmi
from domain.military import military_guidance


class DomainTests(unittest.TestCase):
    def test_calculate_bmi_rounds_to_one_decimal_place(self):
        self.assertEqual(calculate_bmi(170, 65), 22.5)

    def test_calculate_bmi_rejects_non_positive_values(self):
        with self.assertRaises(ValueError):
            calculate_bmi(0, 65)
        with self.assertRaises(ValueError):
            calculate_bmi(170, -1)

    def test_military_guidance_applies_measurement_rounding(self):
        result = military_guidance(170.9, 65.28)
        self.assertEqual(result["height"], "170")
        self.assertEqual(result["weight"], "65.2")
        self.assertEqual(result["bmi"], "22.6")
        self.assertEqual(result["category"], "常備役體位")


if __name__ == "__main__":
    unittest.main()
