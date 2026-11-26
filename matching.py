"""
matching.py - the letter logic.

Everything here takes values in and returns an answer.
Nothing here asks the user anything or prints anything.
"""

# Scrabble points for each letter.
scores = {
    1: ["A", "E", "I", "O", "U", "L", "N", "S", "T", "R"],
    2: ["D", "G"],
    3: ["B", "C", "M", "P"],
    4: ["F", "H", "V", "W", "Y"],
    5: ["K"],
    8: ["J", "X"],
    10: ["Q", "Z"]
}


# ---------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------

def clean(text):
    """Lower case and keep letters only.
    Example: "Dirty room!" -> "dirtyroom"
    """
    return "".join(character for character in text.lower() if character.isalpha())


def sort_letters(text):
    """Return the letters of text in alphabetical order.
    Example: "listen" -> "eilnst"

    Two words are anagrams if their sorted letters are the same.
    """
    letters = list(clean(text))  # "cat" -> ["c", "a", "t"]
    letters.sort()               # ["a", "c", "t"]
    return "".join(letters)      # "act"


def count_letters(text):
    """Count how many times each letter appears.
    Example: "apple" -> {"a": 1, "p": 2, "l": 1, "e": 1}
    """
    counts = {}
    for letter in clean(text):
        counts[letter] = counts.get(letter, 0) + 1
    return counts


def get_count(counts, letter):
    """Return how many times letter appears in counts (0 if it is missing)."""
    if letter in counts:
        return counts[letter]
    else:
        return 0


def can_build(word, available):
    """Return True if word can be made from the available letters.
    available is a dictionary of letter counts, e.g. {"a": 2, "t": 1}.
    """
    needed = count_letters(word)
    for letter in needed:
        if get_count(available, letter) < needed[letter]:
            return False  # Not enough of this letter.
    return True


def fits_inside(word, letters):
    """Same as can_build, but takes the letters as plain text.
    Example: fits_inside("rate", "tares") -> True
    """
    return can_build(word, count_letters(letters))


def total_scores(text):
    """Add up the Scrabble points of every letter in text."""
    total = 0

    text = text.upper()

    for score, letters in scores.items():
        for letter in text:
            if letter in letters:
                total += score

    return total


# ---------------------------------------------------------------
# Level 2 - comparing two words
# ---------------------------------------------------------------

def find_differences(first, second):
    """Use letter counts to find which letters each word has extra.
    Returns two dictionaries: extra in the first, extra in the second.
    Example: "apple", "pale" -> {"p": 1}, {}
    """
    counts_first = count_letters(first)
    counts_second = count_letters(second)

    extra_in_first = {}
    extra_in_second = {}

    all_letters = set(counts_first) | set(counts_second)
    for letter in sorted(all_letters):
        difference = counts_first.get(letter, 0) - counts_second.get(letter, 0)
        if difference > 0:
            extra_in_first[letter] = difference
        elif difference < 0:
            extra_in_second[letter] = -difference

    return extra_in_first, extra_in_second


def find_in_list(word, word_list):
    """Return anagrams of word from any list by checking every word.
    Used for the small built-in list (Level 2)."""
    target = sort_letters(word)

    matches = []
    for candidate in word_list:
        if sort_letters(candidate) == target and clean(candidate) != clean(word):
            matches.append(candidate)
    return matches


# ---------------------------------------------------------------
# Level 3 - using the word list and families
# ---------------------------------------------------------------

def find_anagrams(word, families):
    """Return every word in the list that is an anagram of word
    (not counting the word itself). Uses one dictionary lookup."""
    target = sort_letters(word)
    family = families.get(target, [])

    matches = []
    for candidate in family:
        if candidate != clean(word):
            matches.append(candidate)
    return matches


def buildable_words(letters, words):
    """Return every word that can be made from letters,
    longest first (words of the same length in alphabetical order)."""
    available = count_letters(letters)

    buildable = []
    for word in words:
        if can_build(word, available):
            buildable.append(word)

    # Step 1: sort alphabetically.
    # Step 2: sort by length, longest first. Words of the same length
    #         stay in alphabetical order from step 1.
    buildable.sort()
    buildable.sort(key=len, reverse=True)
    return buildable


# ---------------------------------------------------------------
# Level 4 - Scrabble and two-word anagrams
# ---------------------------------------------------------------

def scrabble_scores(letters, words):
    """Return every buildable word with its score, highest score first.
    Example: [("blaster", 9), ("stable", 8), ...]
    """
    scrabble_report = {}

    for word in words:
        if fits_inside(word, letters):
            scrabble_report[word] = total_scores(word)

    return sorted(scrabble_report.items(), key=lambda item: item[1], reverse=True)


def find_two_word_anagrams(phrase, words, families, limit=20):
    """Return pairs of words that together use exactly the letters
    of the phrase, at most limit pairs."""
    phrase = clean(phrase)

    results = []
    seen = set()

    for word in words:

        if not fits_inside(word, phrase):
            continue

        # Skip words that use all the letters
        if sort_letters(word) == sort_letters(phrase):
            continue

        # Calculate leftover letters
        phrase_counts = count_letters(phrase)
        word_counts = count_letters(word)

        leftover = ""

        for letter, amount in phrase_counts.items():
            remaining = amount - word_counts.get(letter, 0)

            if remaining > 0:
                leftover += letter * remaining

        # Get the sorted key of the leftover
        leftover_key = sort_letters(leftover)

        # Look for words that match the leftover
        partners = families.get(leftover_key, [])

        for partner in partners:

            pair = tuple(sorted([word, partner]))

            if pair not in seen:
                seen.add(pair)
                results.append([word, partner])

            if len(results) >= limit:
                break

        if len(results) >= limit:
            break

    return results
