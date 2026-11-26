"""
data.py - the word file and analysis.

Loading and saving files, the anagram families dictionary,
statistics, the timing comparison and adding new words.
"""

import itertools
import time
from pathlib import Path

from matching import clean, sort_letters, find_anagrams

WORD_FILE = Path(__file__).parent / "words.txt"
REPORT_FILE = Path(__file__).parent / "report.txt"


# ---------------------------------------------------------------
# Loading the word file
# ---------------------------------------------------------------

def load_words(file_path):
    """Read the word file (one word per line).
    Returns a list of clean, unique words, or None if the file
    is missing or empty."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Could not find the word list: {file_path}")
        print("Create a text file with one word per line and try again.")
        return None
    except OSError as error:
        print(f"Could not read the word list: {error}")
        return None

    words = []
    seen = set()
    for line in lines:
        word = clean(line)
        if word and word not in seen:   # skip blank lines and duplicates
            seen.add(word)
            words.append(word)

    if not words:
        print(f"The word list is empty: {file_path}")
        print("Add some words (one per line) and try again.")
        return None

    return words


# ---------------------------------------------------------------
# Anagram families
# ---------------------------------------------------------------

def group_into_families(words):
    """Put words with the same letters into groups ("families").
    Example: ["listen", "silent", "cat", "act"] ->
             {"eilnst": ["listen", "silent"], "act": ["cat", "act"]}
    """
    families = {}
    for word in words:
        key = sort_letters(word)
        if key not in families:
            families[key] = []
        families[key].append(word)
    return families


def largest_families(families):
    """Return the keys of the biggest family (or families, if there is a tie)."""
    # Pass 1: go through every family and remember the biggest size.
    largest_size = 0
    for key in families:
        family = families[key]
        if len(family) > largest_size:
            largest_size = len(family)

    # Pass 2: collect every family that has that size.
    keys = []
    for key in families:
        if len(families[key]) == largest_size:
            keys.append(key)
    return keys


# ---------------------------------------------------------------
# Timing comparison
# ---------------------------------------------------------------

def anagrams_by_permutations(word, word_set):
    """Slow method: try every possible order of the letters and
    keep the ones that are real words in the list."""
    found = set()
    for arrangement in itertools.permutations(clean(word)):
        candidate = "".join(arrangement)
        if candidate in word_set:
            found.add(candidate)
    return found


def anagrams_by_dictionary(word, families):
    """Fast method: sort the letters and do one dictionary lookup."""
    return set(families.get(sort_letters(word), []))


def pick_test_words(words, families):
    """Pick one test word for each length 5 to 9.
    Prefer a word that has anagrams in the list."""
    test_words = []
    for length in range(5, 10):
        chosen = ""
        for word in words:
            if len(word) == length:
                if chosen == "":
                    chosen = word
                if len(families[sort_letters(word)]) > 1:
                    chosen = word
                    break
        if chosen:
            test_words.append(chosen)
    return test_words


def run_timing(words, families):
    """Time both methods for each test word.
    Returns a list of rows: (word, slow time, fast time, same result?)."""
    word_set = set(words)  # a set makes "is this a word?" checks fast

    rows = []
    for word in pick_test_words(words, families):
        start = time.perf_counter()
        slow_result = anagrams_by_permutations(word, word_set)
        slow_time = time.perf_counter() - start

        start = time.perf_counter()
        fast_result = anagrams_by_dictionary(word, families)
        fast_time = time.perf_counter() - start

        rows.append((word, slow_time, fast_time, slow_result == fast_result))
    return rows


# ---------------------------------------------------------------
# Statistics report
# ---------------------------------------------------------------

def build_statistics(words, families):
    """Work out the word-list statistics and return them as a list of lines."""
    # Longest word(s)
    longest_length = 0
    for word in words:
        if len(word) > longest_length:
            longest_length = len(word)
    longest_words = []
    for word in words:
        if len(word) == longest_length:
            longest_words.append(word)

    # Families with at least two words
    real_families = 0
    for key in families:
        if len(families[key]) > 1:
            real_families += 1

    # Most common letters across all words
    letter_totals = {}
    for word in words:
        for letter in word:
            letter_totals[letter] = letter_totals.get(letter, 0) + 1
    top_letters = sorted(letter_totals.items(), key=lambda item: item[1], reverse=True)[:5]

    lines = []
    lines.append("=== Word List Statistics ===")
    lines.append(f"Number of words: {len(words)}")
    lines.append(f"Longest word(s) ({longest_length} letters): " + ", ".join(longest_words))
    lines.append(f"Number of anagram families: {len(families)}")
    lines.append(f"Families with 2 or more words: {real_families}")
    lines.append("Most common letters:")
    for letter, amount in top_letters:
        lines.append(f"  {letter}: {amount}")
    return lines


def save_report(lines):
    """Write the report lines to report.txt.
    Returns True if it worked, False if not."""
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
        return True
    except OSError as error:
        print(f"Could not save the report: {error}")
        return False


# ---------------------------------------------------------------
# Adding new words
# ---------------------------------------------------------------

def add_word(entry, words, families):
    """Add a new word to the word file, the list and the families.
    Returns a message saying what happened."""
    word = entry.strip().lower()

    # Reject empty entries and anything that is not only letters.
    if word == "" or not word.isalpha():
        return "Invalid word - use letters only (no spaces, numbers or symbols)."

    if word in words:
        return f'"{word}" is already in the word list.'

    try:
        # Make sure the file ends with a new line before adding,
        # otherwise the new word would join the last word.
        needs_newline = False
        if WORD_FILE.exists():
            with open(WORD_FILE, "r", encoding="utf-8") as file:
                content = file.read()
            if content and not content.endswith("\n"):
                needs_newline = True

        with open(WORD_FILE, "a", encoding="utf-8") as file:
            if needs_newline:
                file.write("\n")
            file.write(word + "\n")
    except OSError as error:
        return f"Could not save the word: {error}"

    # Keep the program's data up to date too.
    words.append(word)
    key = sort_letters(word)
    if key not in families:
        families[key] = []
    families[key].append(word)

    message = f'"{word}" was added to the word list.'
    others = find_anagrams(word, families)
    if others:
        message += "\n  It joins the family: " + ", ".join(others)
    return message
