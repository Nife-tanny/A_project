# Anagram Finder

**Project 13 · Python (standard library only)**

A command-line tool that checks whether two words or phrases are anagrams, finds every anagram of a word in a word list, and grows into a word-analysis toolkit that builds words from a set of letters, scores them like Scrabble, finds two-word anagrams, and compares the speed of two search methods.

---

## Features

### Level 1: Basic
- Checks whether two words are anagrams (same letters, different order)
- Ignores upper and lower case, and spaces
- Shows the sorted letters used for the comparison
- Treats two identical words as **not** anagrams and explains why
- Repeats until the user chooses to stop

### Level 2: Intermediate
- Ignores punctuation, so phrases work (e.g. *Dormitory* and *Dirty room*)
- Validates input: every entry must contain at least one letter
- When two words are not anagrams, shows which letters are extra in each word
- Menu option to find anagrams in a small built-in word list

### Level 3: Problem Solving
- Loads the word list from `words.txt`, with clear messages if the file is missing or empty
- Groups all words into **anagram families** and shows the largest family (ties are all shown)
- Lists every anagram of a word from the word list, with a count
- Builds every word that can be made from a set of letters

### Level 4: Challenge
- **Scrabble scoring:** given 7 letters, shows the top 10 highest-scoring words
- **Two-word anagrams:** finds pairs of words that use exactly the letters of a phrase (limited to 20 results)
- **Timing comparison:** permutations vs. the sorted-letters dictionary, for words of 5 to 9 letters
- **Statistics report:** word count, longest word(s), number of families, most common letters; saved to `report.txt`
- **Add a word:** adds new words to `words.txt` from the menu, rejecting duplicates and invalid entries

---

## Requirements

- Python 3.6 or newer
- No extra packages: only the Python standard library (`pathlib`, `itertools`, `time`)

---

## How to run

1. Put all the project files in the same folder (see below).
2. Open a terminal in that folder.
3. Run:

```
python main.py
```

On some computers the command is `python3 main.py`.

---

## Project structure

```
anagram-finder/
├── main.py       # Starts the program and runs the menu
├── matching.py   # Letter logic: cleaning, sorting, counting, building, scoring, two-word anagrams
├── display.py    # Prompts, input validation and printing results
├── data.py       # Word file, anagram families, timing, statistics, adding words
├── words.txt     # The word list, one word per line
└── report.txt    # Created by the program (option 9)
```

`matching.py` never prints or asks for input. Its functions take values in and return answers, which keeps the logic easy to test and reuse.

---

## Menu

```
1. Check two words
2. Find anagrams in the built-in list
3. Find all anagrams of a word
4. Show the largest anagram family
5. Build words from these letters
6. Scrabble: best words from 7 letters
7. Find two-word anagrams of a phrase
8. Timing comparison
9. Word list statistics (saves report)
10. Add a new word
0. Quit
```

---

## Example runs

**Checking two words**
```
First word or phrase: Listen
Second word or phrase: Silent

"Listen" and "Silent" are anagrams.
Sorted letters: eilnst
```

**When they are not anagrams**
```
First word or phrase: apple
Second word or phrase: pale

"apple" and "pale" are NOT anagrams.
Sorted letters of the first word:  aelpp
Sorted letters of the second word: aelp
  Extra in the first:  p x1
```

**Largest anagram family**
```
Largest anagram family (6 words, letters: eilnst):
  listen, silent, enlist, tinsel, inlets, elints
Largest anagram family (6 words, letters: opst):
  stop, pots, tops, post, spot, opts
```

**Scrabble (letters R A T E S B L)**
```
25 words can be built; Top 10:
You got a score of 9 for blaster
You got a score of 8 for stable
You got a score of 8 for tables
...
```

**Two-word anagrams**
```
Enter your phrase: dormitory

dirty + room
dirty + moor
```

---

## How it works

### The key idea: sorted letters
If you sort a word's letters alphabetically, every anagram of that word gives the same string:

| Word   | Sorted letters |
|--------|----------------|
| listen | eilnst         |
| silent | eilnst         |
| enlist | eilnst         |

So checking for anagrams becomes comparing two sorted strings.

### Anagram families
When the program starts, it builds one dictionary where each key is a sorted-letters string and each value is the list of words that share it:

```
"eilnst" → ["listen", "silent", "enlist", "tinsel", "inlets", "elints"]
"opst"   → ["stop", "pots", "tops", "post", "spot", "opts"]
```

This dictionary is built **once** and shared by every feature that needs it. Finding all anagrams of a word is then a single lookup.

### Building words from letters
A word can be built if it needs no letter more times than the letters available have it. For example, "rate" fits inside "tares", but "tree" does not (it needs two e's).

### Two-word anagrams
For each word that fits inside the phrase, the program works out the leftover letters, sorts them, and looks them up in the families dictionary. Every word found there forms a pair. Pairs are stored in sorted order in a set, so "dirty + room" and "room + dirty" count once.

### Timing comparison
- **Permutations:** try every order of the letters and keep the real words. The number of orders grows as a factorial: 5 letters = 120, 9 letters = 362,880.
- **Dictionary:** sort the letters and do one lookup, whatever the length.

Both methods return the same anagrams, but the dictionary method stays almost instant while the permutation method slows down sharply as words get longer.

---

## Design decisions

- Words are compared **after cleaning** (lower case, letters only), so "Listen" and "listen" count as the same word.
- Identical words are **not** anagrams, because nothing has been rearranged.
- A word is not listed as an anagram of itself.
- When families tie for largest, **all** of them are shown.
- In Scrabble, words tied at the 10th place cut-off are decided by their order in the word list.
- Two-word anagrams show at most **20** pairs; a word may pair with itself if the letters allow it.
- New words must contain letters only and must not already be in the list.

---

## Word list format

`words.txt` holds one word per line:

```
listen
silent
enlist
...
```

Blank lines and duplicates are ignored when the file is loaded. Words added through option 10 are saved straight to this file.

---

## Limitations

- The program only knows the words in `words.txt`, so results depend on the size of that list.
- It cannot check spelling: any letters-only word can be added.
- Two-word anagrams only look for pairs, not three or more words.

## Possible improvements

- A larger word list
- Three-word anagrams
- Scrabble blank tiles and board bonuses
- A graphical user interface

---

## Team

Kachi, Nifemi and Oluwaseun
