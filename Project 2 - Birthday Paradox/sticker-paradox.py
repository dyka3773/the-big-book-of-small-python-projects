import random
import time

from typing import List, Set


INTRO_TEXT = '''The Sticker Paradox shows us that in a package of 6 stickers, the odds
that at least one of them will already be in your collection is surprisingly high.
This program runs a Monte Carlo simulation to explore this concept.

(It's not actually a paradox, it's just a surprising result.)
'''
NUM_OF_STICKER_PLACES = 728
STICKERS: List[int] = [x for x in range(NUM_OF_STICKER_PLACES)]


def generate_stickers(n: int) -> List[int]:
    """Generates a list of n random stickers.

    Args:
        n (int): Number of stickers to generate.

    Returns:
        list: List of n random stickers.
    """
    stickers: List[int] = random.sample(population=STICKERS, k=n)
    return stickers        

class StickerPack():
    stickers: List[int] = []
    
    def __init__(self) -> None:
        self.stickers = generate_stickers(6)

class Album():
    stickers: Set[int]
    
    def __init__(self, stickers_completed: int = 0) -> None:
        self.stickers = set()
        while len(self.stickers) < stickers_completed:
            self.stickers.add(random.choice(STICKERS))
        
    def is_included(self, sticker: int) -> bool:
        return sticker in self.stickers
        
    def has_any_matches(self, pack: StickerPack) -> bool:
        for sticker in pack.stickers:
            if self.is_included(sticker):
                return True
        return False

    def add_sticker(self, sticker: int) -> None:
        self.stickers.add(sticker)

def print_text_with_delay(text: str, delay: float = 0.03) -> None:
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
    
    num_packs: int = input_num_packs()
    album = Album() # Start with an empty album
    packs: List[StickerPack] = [StickerPack() for _ in range(num_packs)]
    
    for i, pack in enumerate(packs):
        if album.has_any_matches(pack):
            print_text_with_delay(f"Pack {i + 1} contains a sticker you already have!")
            for sticker in pack.stickers:
                if album.is_included(sticker):
                    print_text_with_delay(f"Sticker {sticker} is already in your collection.")
                else:
                    album.add_sticker(sticker)
        else:
            for sticker in pack.stickers:
                album.add_sticker(sticker)
            print_text_with_delay(f"Pack {i + 1} contains all new stickers!")
            
    print_text_with_delay("All packs have been opened.")
    print_text_with_delay(f"You have {len(album.stickers)} unique stickers in your collection.")
    
    print_text_with_delay("Here are the stickers you have:")
    print(album.stickers)
    print_text_with_delay(f"You need {len(STICKERS) - len(album.stickers)} more stickers to complete your collection.") 
    
    print_text_with_delay("Now let's see how many more packs you need to complete your collection.")
    packs_needed = 0
    while len(album.stickers) < len(STICKERS):
        packs_needed += 1
        pack = StickerPack()
        for sticker in pack.stickers:
                album.add_sticker(sticker)
                print('.', end='')
            
    print_text_with_delay(f"\n\nYou need {packs_needed} more packs to complete your collection.")
    
    del album
    
    print_text_with_delay("""

Let's also run a Monte Carlo simulation to see how many packs
you would need on average to complete your collection.""")
    print_text_with_delay("""
During each simulation, we will also calculate how many packs you would need
on average to find your first duplicate sticker.""")
    print_text_with_delay("(This will take a while...)")
    input("Press Enter to continue...")

    packs_needed_per_compl_sim = []
    packs_needed_per_first_sim = []
    for i in range(100):
        packs_needed = 1
        duplicate_found = False
        album = Album()
        pack = StickerPack()
        while len(album.stickers) < len(STICKERS):
            if album.has_any_matches(pack) and duplicate_found == False:
                packs_needed_per_first_sim.append(packs_needed)
                duplicate_found = True
            for sticker in pack.stickers:
                album.add_sticker(sticker)
            pack = StickerPack()
            packs_needed += 1
        
        packs_needed_per_compl_sim.append(packs_needed)
        
        if i % 10 == 0:
            print_text_with_delay(f"{i} simulations run...")
    
    average_packs_needed_for_completion = sum(packs_needed_per_compl_sim) / len(packs_needed_per_compl_sim)
    average_packs_needed_for_first_duplicate = sum(packs_needed_per_first_sim) / len(packs_needed_per_first_sim)
    print_text_with_delay(f"On average, you would need to open {average_packs_needed_for_completion:.2f} packs to complete your collection.")
    print_text_with_delay(f"During each simulation, you would need to open {average_packs_needed_for_first_duplicate:.2f} packs to find your first duplicate sticker.")
    print_text_with_delay("These are probably higher than you would expect!")
    
    
    print_text_with_delay(f"""\n\nLet's also run a Monte Carlo simulation to see what the probability is
that you will find a duplicate sticker if you start with {num_packs} packs.""")
    print_text_with_delay("(This will take a while...)")
    input("Press Enter to continue...")
    
    matches = 0
    for i in range(100_000):
        album = Album()
        packs = [StickerPack() for _ in range(num_packs)]
        for pack in packs:
            if album.has_any_matches(pack):
                matches += 1
                break
            for sticker in pack.stickers:
                album.add_sticker(sticker)
        if i % 10_000 == 0:
            print_text_with_delay(f"{i} simulations run...")
            
    print_text_with_delay(
        f"{matches} simulations had at least one shared sticker.")
    print_text_with_delay(
        f"Probability of at least one duplicate sticker when starting with {num_packs} packs: {matches / 1000:.2f}%")
    print_text_with_delay("That's probably higher than you would expect!")


def input_num_packs() -> int:
    """Prompt the user for the number of sticker packs to generate.

    Returns:
        int: The number of sticker packs to generate
    """
    while True:
        print_text_with_delay("How many sticker packs shall I generate?")
        print_text_with_delay("(Numbers larger than 15 can take a while.)")
        response = input('> ')
        if response.isdecimal() and (1 < int(response)):
            num_packs = int(response)
            break
        else:
            print_text_with_delay("Please enter a number greater than 1.")
    return num_packs

if __name__ == "__main__":
    main()
