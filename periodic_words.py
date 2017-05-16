from collections import defaultdict
import sys

class Trie:

    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.chars = {c for letter in alphabet for c in letter}
        self.subtries = defaultdict(lambda: Trie(alphabet))
        self.is_word = False

    def add_word(self, word):
        if set(word) - self.chars:
            return False # unrepresentable letters
        if not word:
            self.is_word = True
            return True
        possible_splits = [1, 2, 3]
        valid = False
        for s in possible_splits:
            split = word[:s]
            if split in self.alphabet:
                valid |= self.subtries[split].add_word(word[s:])
        return valid

    def add_words(self, words):
        for w in words:
            self.add_word(w)

    def get_all_words(self, with_capitalization):
        return sorted(self._get_all_words(with_capitalization), key=len, reverse=True)

    def _get_all_words(self, with_capitalization, prefix=""):
        words = {prefix} if self.is_word else set()
        for letter, trie in self.subtries.items():
            suffix = letter.capitalize() if with_capitalization else letter
            words.update(trie._get_all_words(with_capitalization, prefix+suffix))
        return words
                

def main(word_file):
    elements = read_elements()
    words = read_words(word_file)
    trie = Trie(elements)
    trie.add_words(words)
    print(trie.get_all_words(False)[:10])


def read_elements():
    with open("elements.txt") as elements_file:
        return {e.strip().lower() for e in elements_file}

def read_words(word_file_path):
    with open(word_file_path) as words_file:
        return [w.strip().lower() for w in words_file if "'" not in w]

if __name__ == '__main__':
    main(sys.argv[1])
