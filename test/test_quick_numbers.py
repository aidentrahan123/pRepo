"""Tests for the quick_numbers demo.

Standard library only — run with:
    python3 -m unittest discover -s test
"""

import io
import sys
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

# Make the demo package importable without installing anything.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "demo"))

import quick_numbers  # noqa: E402


class TestQuickNumbers(unittest.TestCase):
    def test_facts_list_is_nonempty(self):
        self.assertTrue(quick_numbers.NUMBER_FACTS)
        self.assertTrue(all(isinstance(f, str) and f for f in quick_numbers.NUMBER_FACTS))

    def test_random_fact_comes_from_list(self):
        # Sample many times; every result must be a known fact.
        for _ in range(100):
            self.assertIn(quick_numbers.random.choice(quick_numbers.NUMBER_FACTS),
                          quick_numbers.NUMBER_FACTS)

    def test_day_of_year_in_valid_range(self):
        day_of_year = date.today().timetuple().tm_yday
        self.assertGreaterEqual(day_of_year, 1)
        self.assertLessEqual(day_of_year, 366)

    def test_main_prints_expected_dashboard(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            quick_numbers.main()
        output = buffer.getvalue()

        self.assertIn("QUICK NUMBERS", output)
        self.assertIn("Today's date", output)
        self.assertIn("Day of year", output)
        self.assertIn("Number fact", output)
        # The printed fact should be one from the list.
        self.assertTrue(any(fact in output for fact in quick_numbers.NUMBER_FACTS))


if __name__ == "__main__":
    unittest.main()
