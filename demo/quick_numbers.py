"""Quick Numbers — prints a few number facts when run.

Standard library only.
"""

import random
from datetime import date

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


def main():
    today = date.today()

    long_date = today.strftime("%A, %B %d, %Y")
    day_of_year = today.timetuple().tm_yday
    number_fact = random.choice(NUMBER_FACTS)

    print("=" * 50)
    print("           QUICK NUMBERS")
    print("=" * 50)
    print(f"Today's date : {long_date}")
    print(f"Day of year  : {day_of_year}")
    print(f"Number fact  : {number_fact}")
    print("=" * 50)


if __name__ == "__main__":
    main()
