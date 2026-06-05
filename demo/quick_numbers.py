"""Quick Numbers — prints a few number facts when run.

Standard library only.

Usage:
    python3 quick_numbers.py            # plain-text dashboard in the terminal
    python3 quick_numbers.py --html     # write quick_numbers.html and open it
    python3 quick_numbers.py --html --no-open   # write the file, don't open
"""

import argparse
import html
import random
import webbrowser
from datetime import date
from pathlib import Path

NUMBER_FACTS = [
    "Zero is the only number that can't be represented in Roman numerals.",
    "A 'googol' is a 1 followed by 100 zeros.",
    "The number 7 is the most commonly chosen 'random' number between 1 and 10.",
    "Any number divisible by 3 has digits that also sum to a multiple of 3.",
    "Pi has been calculated to over 100 trillion decimal places.",
    "The sum of the first n odd numbers is always a perfect square.",
    "111,111,111 x 111,111,111 = 12,345,678,987,654,321.",
    "A 'perfect number' equals the sum of its divisors — 6 is the smallest.",
]

OUTPUT_FILE = "quick_numbers.html"


def gather_facts():
    """Return the dashboard data as a dict (date, day-of-year, random fact)."""
    today = date.today()
    return {
        "long_date": today.strftime("%A, %B %d, %Y"),
        "day_of_year": today.timetuple().tm_yday,
        "number_fact": random.choice(NUMBER_FACTS),
    }


def render_text(data):
    """Build the plain-text dashboard string."""
    lines = [
        "=" * 50,
        "           QUICK NUMBERS",
        "=" * 50,
        f"Today's date : {data['long_date']}",
        f"Day of year  : {data['day_of_year']}",
        f"Number fact  : {data['number_fact']}",
        "=" * 50,
    ]
    return "\n".join(lines)


def render_html(data):
    """Build a styled, self-contained HTML page string."""
    long_date = html.escape(data["long_date"])
    day_of_year = html.escape(str(data["day_of_year"]))
    number_fact = html.escape(data["number_fact"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Quick Numbers</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #1e3c72, #2a5298);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #1a1a1a;
    }}
    .card {{
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
      padding: 2.5rem 3rem;
      max-width: 520px;
      width: 90%;
    }}
    h1 {{
      margin: 0 0 1.5rem;
      font-size: 1.8rem;
      letter-spacing: 0.05em;
      text-align: center;
      color: #2a5298;
    }}
    .row {{
      display: flex;
      justify-content: space-between;
      padding: 0.75rem 0;
      border-bottom: 1px solid #eee;
    }}
    .row:last-child {{
      border-bottom: none;
      flex-direction: column;
    }}
    .label {{
      font-weight: 600;
      color: #555;
    }}
    .value {{
      color: #111;
      text-align: right;
    }}
    .fact {{
      margin-top: 0.5rem;
      font-size: 1.1rem;
      line-height: 1.5;
      color: #2a5298;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>QUICK NUMBERS</h1>
    <div class="row">
      <span class="label">Today's date</span>
      <span class="value">{long_date}</span>
    </div>
    <div class="row">
      <span class="label">Day of year</span>
      <span class="value">{day_of_year}</span>
    </div>
    <div class="row">
      <span class="label">Number fact</span>
      <span class="fact">{number_fact}</span>
    </div>
  </div>
</body>
</html>
"""


def write_html(data, path=OUTPUT_FILE):
    """Render the HTML page and write it to `path`. Returns the resolved Path."""
    output_path = Path(path).resolve()
    output_path.write_text(render_html(data), encoding="utf-8")
    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print quick number facts.")
    parser.add_argument(
        "--html",
        action="store_true",
        help="write a styled HTML page instead of plain text",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="with --html, write the file but do not open it in a browser",
    )
    args = parser.parse_args(argv)

    data = gather_facts()

    if args.html:
        output_path = write_html(data)
        print(f"Wrote {output_path}")
        if not args.no_open:
            webbrowser.open(output_path.as_uri())
    else:
        print(render_text(data))


if __name__ == "__main__":
    main()
