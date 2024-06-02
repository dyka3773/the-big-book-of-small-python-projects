import random
import time

NUM_DIGITS = 3
MAX_GUESSES = 10

INTRO_MESSAGE = f'''Bagels, a deductive logic game.
I am thinking of a {NUM_DIGITS}-digit number with no repeated digits.
Try to guess what it is. Here are some clues:
When I say:    That means:
  Pico         One digit is correct but in the wrong position.
  Fermi        One digit is correct and in the right position.
  Bagels       No digit is correct.

For example, if the secret number was 248 and your guess was 843, the clues would be Fermi Pico.
'''


def print_text_with_delay(text: str, delay: float = 0.05) -> None:
    """Print text with a delay between each word.

    Args:
        text (str): The text to print.
        delay (float, optional): The delay between each word in seconds. Defaults to 0.05.
    """
    for word in text.split(' '):
        print(word, end=' ', flush=True)
        time.sleep(delay)
    print()


def get_secret_num() -> str:
    """Generate a random secret number with NUM_DIGITS digits.

    Returns:
        str: A string of NUM_DIGITS digits, each digit is unique.
    """
    digits = list('0123456789')
    random.shuffle(digits)
    secret_num = ''
    for i in range(NUM_DIGITS):
        secret_num += digits[i]
    return secret_num


def get_clues(secret_num: str, guess: str) -> list[str]:
    """Return a list of clues for the guess based on the secret number.
    The possible clues are 'Fermi', 'Pico', and 'Bagels'.

    Args:
        secret_num (str): The secret number.
        guess (str): The guess.

    Returns:
        list[str]: A list of clues.
    """
    clues: list[str] = []

    for i in range(NUM_DIGITS):
        if guess[i] == secret_num[i]:
            clues.append('Fermi')
        elif guess[i] in secret_num:
            clues.append('Pico')
    if not clues:
        clues.append('Bagels')

    # Sort the clues so that they appear in alphabetical order and not give away the position of numbers.
    clues.sort()

    return clues


def main() -> None:
    print_text_with_delay(INTRO_MESSAGE)

    while True:  # Main game loop
        secret_num = get_secret_num()

        print_text_with_delay(
            f'I have thought up a number. You have {MAX_GUESSES} guesses to get it.')

        for guesses_attemped in range(MAX_GUESSES):
            guess = ''
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print_text_with_delay(f'Guess #{guesses_attemped+1}.')
                guess = input('> ')

            clues = get_clues(secret_num, guess)

            print_text_with_delay(' '.join(clues))

            if guess == secret_num:
                print_text_with_delay(
                    f'You got it in {guesses_attemped+1} guesses!')
                break
        else:
            print_text_with_delay(
                f'You ran out of guesses. The answer was {secret_num}.')

        print_text_with_delay('Do you want to play again? (y or n)')
        if not input('> ').lower().startswith('y'):
            break

    print_text_with_delay('Thanks for playing!')


if __name__ == '__main__':
    main()
