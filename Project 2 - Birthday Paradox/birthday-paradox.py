import datetime
import random
import time

from typing import List, Set


INTRO_TEXT = '''The Birthday Paradox shows us that in a group of N people, the odds
that at least two of them have the same birthday is surprisingly high. This
program runs a Monte Carlo simulation to explore this concept.

(It's not actually a paradox, it's just a surprising result.)
'''
MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
)


def generate_birthdays(n: int) -> List[datetime.date]:
    """Generates a list of n random birthdays.

    Args:
        n (int): Number of birthdays to generate.

    Returns:
        list: List of n random birthdays.
    """
    birthdays = []
    for _ in range(n):
        # NOTE: The year 2000 is a leap year, this might affect the results.
        first_day = datetime.date(2000, 1, 1)

        random_day = first_day + \
            datetime.timedelta(days=random.randint(1, 365))
        birthdays.append(random_day)
    return birthdays


def has_matches(birthdays: List[datetime.date]) -> bool:
    """Check if there are any duplicate birthdays in the list.

    Args:
        birthdays (list): List of birthdays.

    Returns:
        bool: True if there is at least one duplicate, False otherwise.
    """
    return len(birthdays) != len(set(birthdays))


def get_duplicates(birthdays: List[datetime.date]) -> List[None] | Set[datetime.date]:
    """Returns a list of duplicate birthdays.

    Args:
        birthdays (list): List of birthdays.

    Returns:
        list: List of duplicate birthdays.
    """
    # This is a quick way to avoid checking for duplicates if there are none.
    if len(birthdays) == len(set(birthdays)):
        return []

    duplicates = []
    for i in range(len(birthdays)):
        for j in range(i + 1, len(birthdays)):
            if birthdays[i] == birthdays[j]:
                duplicates.append(birthdays[i])
    return set(duplicates)


def print_text_with_delay(text: str, delay: float = 0.035) -> None:
    """Print text with a delay between each word.

    Args:
        text (str): The text to print.
        delay (float, optional): The delay between each word in seconds. Defaults to 0.05.
    """
    for word in text.split(' '):
        print(word, end=' ', flush=True)
        time.sleep(delay)
    print()


def main() -> None:
    print_text_with_delay(INTRO_TEXT)
    num_birthdays = input_num_birthdays()

    birthdays = generate_birthdays(num_birthdays)

    print_text_with_delay(f"Here are {num_birthdays} birthdays:")

    for i, birthday in enumerate(birthdays):
        print_text_with_delay(
            f"Person {i + 1}: {MONTHS[birthday.month - 1]} {birthday.day}")

    duplicates = get_duplicates(birthdays)

    if duplicates:
        print_text_with_delay(
            "Same birthday for multiple people on these dates:")
        for duplicate in duplicates:
            print_text_with_delay(
                f"{MONTHS[duplicate.month - 1]} {duplicate.day}")  # type: ignore
    else:
        print_text_with_delay("No shared birthdays in this group.")

    print_text_with_delay(
        f"Generating {num_birthdays} random birthdays 100,000 times...")
    input("Press Enter to continue...")

    matches = 0

    for i in range(100_000):
        if i % 10_000 == 0:
            print_text_with_delay(f"{i} simulations run...")
        birthdays = generate_birthdays(num_birthdays)
        if has_matches(birthdays):  # type: ignore
            matches += 1

    print_text_with_delay("100,000 simulations run.")
    print_text_with_delay(
        f"{matches} simulations had at least one shared birthday.")
    print_text_with_delay(
        f"Probability of at least one shared birthday: {matches / 1000:.2f}%")
    print_text_with_delay("That's probably higher than you would expect!")


def input_num_birthdays() -> int:
    """Prompt the user for the number of birthdays to generate.

    Returns:
        int: The number of birthdays to generate (between 1 and 100).
    """
    while True:
        print_text_with_delay("How many birthdays shall I generate? (Max 100)")
        response = input('> ')
        if response.isdecimal() and (1 <= int(response) <= 100):
            num_birthdays = int(response)
            break
        else:
            print_text_with_delay("Please enter a number between 1 and 100.")
    return num_birthdays


if __name__ == "__main__":
    main()
