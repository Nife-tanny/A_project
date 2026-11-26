"""
Project 13 - Anagram Finder
A command-line tool that checks anagrams, finds anagram families,
builds words from letters, scores them like Scrabble, and more.

Standard library only. Run this file to start the program:
    python main.py

Files:
    main.py      - starts the program and runs the menu
    matching.py  - letter logic (no input or printing)
    display.py   - prompts, validation and printing results
    data.py      - word file, families, timing, statistics, adding words
    words.txt    - the word list, one word per line
"""

from data import WORD_FILE, load_words, group_into_families
import display


def main():
    print("=== Anagram Finder ===")

    words = load_words(WORD_FILE)
    if words is None:
        return  # Stop: the word list could not be loaded.

    # Built once here and shared with every option that needs it.
    families = group_into_families(words)

    print(f"Loaded {len(words)} words.")

    while True:
        print()
        print("1. Check two words")
        print("2. Find anagrams in the built-in list")
        print("3. Find all anagrams of a word")
        print("4. Show the largest anagram family")
        print("5. Build words from these letters")
        print("6. Scrabble: best words from 7 letters")
        print("7. Find two-word anagrams of a phrase")
        print("8. Timing comparison")
        print("9. Word list statistics (saves report)")
        print("10. Add a new word")
        print("0. Quit")
        choice = input("Choose 0-10: ").strip()

        if choice == "1":
            display.check_two_words()
        elif choice == "2":
            display.find_in_built_in_list()
        elif choice == "3":
            display.show_anagrams_of_word(families)
        elif choice == "4":
            display.show_largest_family(families)
        elif choice == "5":
            display.show_buildable_words(words)
        elif choice == "6":
            display.show_scrabble_words(words)
        elif choice == "7":
            display.show_two_word_anagrams(words, families)
        elif choice == "8":
            display.show_timing(words, families)
        elif choice == "9":
            display.show_statistics(words, families)
        elif choice == "10":
            display.ask_and_add_word(words, families)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("  Please choose a number from 0 to 10.")


if __name__ == "__main__":
    main()
