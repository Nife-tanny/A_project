"""
display.py - talking to the user.

Prompts, input validation and printing results.
The letter logic lives in matching.py and the file work in data.py.
"""

from matching import (clean, sort_letters, find_differences, find_in_list,
                      find_anagrams, buildable_words, scrabble_scores,
                      find_two_word_anagrams)
from data import largest_families, run_timing, build_statistics, save_report, add_word, REPORT_FILE

# Small word list built into the program (used by option 2, from Level 2).
BUILT_IN_WORDS = [
    "listen", "silent", "enlist", "tinsel", "inlets",
    "stone", "notes", "onset", "tones", "stop", "pots", "tops", "post", "spot",
    "evil", "vile", "live", "veil", "race", "care", "acre",
    "heart", "earth", "hater", "night", "thing", "dusty", "study",
]


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------

def ask_for_text(prompt):
    """Keep asking until the entry contains at least one letter."""
    while True:
        text = input(prompt)
        if clean(text):
            return text
        print("  Please enter at least one letter.")


def ask_yes_no(prompt):
    """Keep asking until the user answers yes or no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False
        print("  Please answer y or n.")


def ask_for_rack():
    """Keep asking until the user enters exactly 7 letters."""
    while True:
        letters = clean(input("Enter 7 letters: "))
        if len(letters) == 7:
            return letters
        else:
            print("Letters should be exactly 7 in number")


def format_counts(counts):
    """Turn {"p": 1, "s": 2} into "p x1, s x2"."""
    return ", ".join(f"{letter} x{number}" for letter, number in counts.items())


# ---------------------------------------------------------------
# Levels 1 and 2
# ---------------------------------------------------------------

def check_pair(first, second):
    """Check one pair of words and print the result."""
    if clean(first) == clean(second):
        print(f'\n"{first}" and "{second}" use the same letters in the same order, '
              "so they are not anagrams.")
        print(f"Sorted letters: {sort_letters(first)}")
        return

    if sort_letters(first) == sort_letters(second):
        print(f'\n"{first}" and "{second}" are anagrams.')
        print(f"Sorted letters: {sort_letters(first)}")
        return

    print(f'\n"{first}" and "{second}" are NOT anagrams.')
    print(f"Sorted letters of the first word:  {sort_letters(first)}")
    print(f"Sorted letters of the second word: {sort_letters(second)}")

    extra_in_first, extra_in_second = find_differences(first, second)

    if extra_in_first:
        print(f"  Extra in the first:  {format_counts(extra_in_first)}")
    if extra_in_second:
        print(f"  Extra in the second: {format_counts(extra_in_second)}")


def check_two_words():
    """Option 1: check pairs of words until the user wants to stop."""
    while True:
        print()
        first = ask_for_text("First word or phrase: ")
        second = ask_for_text("Second word or phrase: ")

        check_pair(first, second)

        if not ask_yes_no("\nCheck another pair? (y/n): "):
            break


def find_in_built_in_list():
    """Option 2: find anagrams of a word in the small built-in list."""
    word = ask_for_text("Word to find anagrams of: ")
    matches = find_in_list(word, BUILT_IN_WORDS)

    if matches:
        print(f"\nFound {len(matches)} anagram(s) of \"{word}\": {', '.join(matches)}")
    else:
        print(f'\nNo anagrams of "{word}" found in the built-in list.')


# ---------------------------------------------------------------
# Level 3
# ---------------------------------------------------------------

def show_anagrams_of_word(families):
    """Option 3: list every anagram of a word from the word list."""
    word = ask_for_text("Word to find anagrams of: ")
    matches = find_anagrams(word, families)

    print()
    if len(matches) > 0:
        print("Found " + str(len(matches)) + ' anagram(s) of "' + word + '":')
        for match in matches:
            print("  " + match)
    else:
        print('Found 0 anagrams of "' + word + '" in the word list.')


def show_largest_family(families):
    """Option 4: show the biggest group of words that are all anagrams.
    If several families tie for biggest, all of them are shown."""
    keys = largest_families(families)

    print()
    if len(families[keys[0]]) < 2:
        print("No anagram families found - every word is unique.")
        return

    for key in keys:
        family = families[key]
        print("Largest anagram family (" + str(len(family)) + " words, letters: " + key + "):")
        print("  " + ", ".join(family))


def show_buildable_words(words):
    """Option 5: find every word that can be made from the user's letters."""
    letters = clean(ask_for_text("Enter your letters: "))
    buildable = buildable_words(letters, words)

    print()
    if len(buildable) > 0:
        print("You can build " + str(len(buildable)) + ' word(s) from "' + letters + '":')
        print("  " + ", ".join(buildable))
    else:
        print("No words in the list can be built from those letters.")


# ---------------------------------------------------------------
# Level 4
# ---------------------------------------------------------------

def show_scrabble_words(words):
    """Option 6: given 7 letters, show the highest-scoring words."""
    letters = ask_for_rack()
    results = scrabble_scores(letters, words)

    print()
    if len(results) == 0:
        print("No words can be built")
        return

    print(f"{len(results)} words can be built; Top 10: ")
    for word, total in results[:10]:
        print(f"You got a score of {total} for {word}")


def show_two_word_anagrams(words, families, limit=20):
    """Option 7: find pairs of words that use exactly the phrase's letters."""
    phrase = ask_for_text("Enter your phrase: ")
    results = find_two_word_anagrams(phrase, words, families, limit)

    print()
    if results:
        for first, second in results:
            print(first, "+", second)
    else:
        print("No two-word anagrams found.")

    if len(results) >= limit:
        print("Showing the first", limit, "results.")


def show_timing(words, families):
    """Option 8: show the timing comparison table."""
    print()
    print("Timing two ways of finding anagrams (please wait)...")
    rows = run_timing(words, families)

    if not rows:
        print("No words of 5 to 9 letters in the list to test.")
        return

    print()
    print(f"{'Length':<8}{'Word':<12}{'Permutations':>14}{'Dictionary':>14}{'Same result?':>14}")
    print("-" * 62)
    for word, slow_time, fast_time, same in rows:
        same_text = "yes" if same else "NO"
        print(f"{len(word):<8}{word:<12}{slow_time:>13.5f}s{fast_time:>13.6f}s{same_text:>14}")

    print()
    print("Permutations grow very fast: 5 letters = 120 orders, 9 letters = 362,880.")
    print("The dictionary method is always just one lookup, whatever the length.")


def show_statistics(words, families):
    """Option 9: show statistics and save them to report.txt."""
    lines = build_statistics(words, families)

    print()
    for line in lines:
        print(line)

    if save_report(lines):
        print()
        print(f"Report saved to {REPORT_FILE.name}")


def ask_and_add_word(words, families):
    """Option 10: ask for a new word and add it."""
    entry = input("Enter a new word: ")
    print("  " + add_word(entry, words, families))
