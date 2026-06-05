"""Tests for the quick_numbers demo.

Standard library only — run with:
    python3 -m unittest discover -s test
"""

import io
import sys
import tempfile
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

    def test_gather_facts_shape(self):
        data = quick_numbers.gather_facts()
        self.assertEqual(
            set(data),
            {"long_date", "day_of_year", "lucky_number", "number_fact"},
        )
        self.assertIn(data["number_fact"], quick_numbers.NUMBER_FACTS)
        self.assertGreaterEqual(data["day_of_year"], 1)
        self.assertLessEqual(data["day_of_year"], 366)

    def test_lucky_number_in_valid_range(self):
        # Sample many times; the lucky number must always be 1..99.
        for _ in range(100):
            lucky = quick_numbers.gather_facts()["lucky_number"]
            self.assertGreaterEqual(lucky, 1)
            self.assertLessEqual(lucky, 99)

    def test_day_of_year_in_valid_range(self):
        day_of_year = date.today().timetuple().tm_yday
        self.assertGreaterEqual(day_of_year, 1)
        self.assertLessEqual(day_of_year, 366)

    def test_render_text_contains_dashboard(self):
        data = quick_numbers.gather_facts()
        output = quick_numbers.render_text(data)
        self.assertIn("QUICK NUMBERS", output)
        self.assertIn("Today's date", output)
        self.assertIn("Day of year", output)
        self.assertIn("Lucky number", output)
        self.assertIn("Number fact", output)
        self.assertIn(data["number_fact"], output)

    def test_render_html_is_valid_page(self):
        data = quick_numbers.gather_facts()
        page = quick_numbers.render_html(data)
        self.assertTrue(page.lstrip().startswith("<!DOCTYPE html>"))
        self.assertIn("<title>Quick Numbers</title>", page)
        self.assertIn("QUICK NUMBERS", page)
        self.assertIn(data["long_date"], page)
        self.assertIn(str(data["day_of_year"]), page)

    def test_render_html_escapes_special_characters(self):
        data = {"long_date": "X & Y", "day_of_year": 1, "lucky_number": 7,
                "number_fact": "<script>"}
        page = quick_numbers.render_html(data)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("X &amp; Y", page)

    def test_write_html_creates_file(self):
        data = quick_numbers.gather_facts()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out.html"
            result = quick_numbers.write_html(data, target)
            self.assertTrue(result.exists())
            self.assertIn("<!DOCTYPE html>", result.read_text(encoding="utf-8"))

    def test_main_text_mode_prints_dashboard(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            quick_numbers.main([])
        output = buffer.getvalue()
        self.assertIn("QUICK NUMBERS", output)
        self.assertTrue(any(fact in output for fact in quick_numbers.NUMBER_FACTS))


if __name__ == "__main__":
    unittest.main()
