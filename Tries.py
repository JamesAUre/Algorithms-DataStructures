# ***********************************
# CODE MADE BY JAMES ANDREW URE
# FIT 2004 ASSIGNMENT 3 SUBMISSION
# COMPLETED 5/18/2020
# ***********************************


class Trie:
    def __init__(self, text):
        """
        Constructor for making a trie, initializes 26 empty pointers that may store a node

        It was necessary to make 26 child nodes as otherwise it would take linear time to search for a node
        :Time complexity (worst case): O(T) where T is the total number of characters across all strings in text
        :Auxiliary space (worst case): O(T) where T is the total number of characters across all strings in text
        :param text: A list containing strings of lowercase words
        """

        # Attributes
        self.children = []
        self.totalwords = 0

        # All children of trie root are trie nodes
        #for i in range(26):
        #    self.children.append(TrieNode())

        self.children = [None] * 26
        # Adding text into trie
        for word in text:
            self.totalwords += 1
            letter = word[0]
            wordlen = len(word)-1
            if self.children[(ord(letter)-97)%26] is None:
                self.children[(ord(letter)-97)%26] = TrieNode()

            self.children[(ord(letter) - 97) % 26].add(0, word, wordlen, "")

    def string_freq(self, query_str):
        """
        Function to check how many times the word has been inserted into the Trie

        :Time complexity (worst case): O(q) where q is the number of characters in query_str
        :Auxiliary space (worst case): O(q) where q is the number of characters in query_str (because
        it recursively traverses word_exists in TrieNode class, adding onto the stack
        :param query_str: A string that the trie will search its frequency of occurrence in text for
        :return: An integer of the number of times query_str occurred in text
        """

        # First letter of the query
        letter = query_str[0]

        # Length of the word (starting from length 0)
        wordlen = len(query_str) - 1
        return self.children[(ord(letter) - 97) % 26].word_exists(0, query_str, wordlen)

    def prefix_freq(self, query_str):
        """
        Function to check how many words query_str is a prefix of amongst the words in text

        :Time complexity (worst case): O(q) where q is the number of characters in query_str
        :Auxiliary space (worst case): O(q) where q is the number of characters in query_str
        :param query_str: A string of lowercase characters that the trie will check how many
        words its a prefix of amongst the words in text
        :return: An integer of the number of words query_str is a prefix of in text
        """

        # If prefix contains characters, traverse nodes
        if len(query_str) > 0:
            letter = query_str[0]
            wordlen = len(query_str) - 1
            return self.children[(ord(letter) - 97) % 26].prefix_exists(0, query_str, wordlen)

        # If prefix is empty, number of every word in the trie
        else:
            return self.totalwords

    def wildcard_prefix_freq(self, query_str):
        """
        Function to check how many words in query_str is a prefix of amongst the words in text, however
        query_str may contain one '?' character representing any character.

        :Time complexity (worst case): O(q + S) where q is the number of characters in query_str and
        S is the number of total number of characters across all strings in text
        :Auxiliary space (worst case): O(S + W) where S is the maximum depth of the trie
        and W is the number of elements in wild_cards
        :param query_str: A string of lowercase characters and one ? character
        :return: A list of strings of the words in text that query_str is a wildcard prefix of
        """

        # Initialize wild_ind
        wild_ind = 0

        # Find "?" character and set its position in wild_ind
        for i in range(len(query_str)):
            if query_str[i] == "?":
                wild_ind = i
                break

        # Initialize list containing split query_str
        strings_split = ["", ""]

        # Characters before and including "?"
        strings_split[0] = query_str[:wild_ind + 1]

        # Characters after "?"
        strings_split[1] = query_str[1 + wild_ind:]

        # Initialize output, list of wildcards found
        wild_cards = []

        # If query starts with "?", jump straight to wildcard found function
        if strings_split[0] == "?":
            for wildcard_letter in range(26):
                wild_cards = self.children[wildcard_letter].wildcard_found(strings_split, wild_cards)

        # Otherwise start traversing trie until "?" is found
        else:
            string_len = len(strings_split[0])-1
            wild_cards = self.children[(ord(strings_split[0][0])-97) % 26].\
                wildcard_exists_first(0, strings_split, string_len, wild_cards)
        return wild_cards


class TrieNode:
    def __init__(self):
        """
        Constructor for making a trie node
        Each node stores the character that's inserted, the word the node represents,
        the number of times that word appears in text, the number of times that prefix appears in text,
        the nodes children and whether it has children

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        """

        # Attributes
        self.letter = None
        self.word = None
        self.wordfreq = 0
        self.prefixfreq = 0
        self.children = []
        self.haschild = False

    def add(self, letter_ind, word, wordlen, node_word):
        """
        Function to add a character into the node

        :Time complexity (worst case): O(T) where T is the total number of characters in word
        :Auxiliary space (worst case): O(T) where T is the total number of characters in word
        :param letter_ind: The character index of word that will be inserted into the node
        :param word: The string containing the character to be inserted
        :param wordlen: The number of characters in word
        :param node_word: The string which the node represents (not the full word unless its reached the end of traversal)
        :return: if its added all characters in word
        """

        # Increments number of prefixes after every times its added something
        self.prefixfreq += 1
        node_word = node_word + word[letter_ind]

        # To indicate node now has a child
        if self.haschild is False:
            self.haschild = True

        # Node now has child nodes and a value
        if self.letter is None:
            # for i in range(26):
            #    self.children.append(TrieNode())
            self.children = [None] * 26
            self.letter = word[letter_ind]

        # If it's reached the end of a word, this node represents a word, increment word counter by 1
        if letter_ind == wordlen:
            self.wordfreq += 1
            if self.word is None:
                self.word = node_word
            return

        # ADD OBJECT IF NOT NONE
        self.children[(ord(word[letter_ind+1]) - 97) % 26].add(letter_ind+1, word, wordlen, node_word)

    def word_exists(self, letter_ind, word, wordlen):
        """
        Function to recursively check amongst node traversal the occurrence word appeared in text

        :Time complexity (worst case): O(q) where q is the number of characters in word
        :Auxiliary space (worst case): O(q) where q is the number of characters in word
        :param letter_ind: The character index of word to indicate the character to search for in the trie
        :param word: Contains the string that is being searched for within this traversal
        :param wordlen: The number of characters in word
        :return: The number of times word has been inserted into the Trie
        """

        # Traversing through all letters in the query will mean the last node stores the counter of word occurrence
        if letter_ind == wordlen:
            return self.wordfreq

        # If the word does not exist in the trie
        elif self.letter != word[letter_ind]:
            return 0

        return self.children[(ord(word[letter_ind+1]) - 97) % 26].word_exists(letter_ind+1, word, wordlen)

    def prefix_exists(self, letter_ind, word, wordlen):
        """
        Function to recursively check amongst node traversal the occurrence word was a frequency of strings in text

        :Time complexity (worst case): O(q) where q is the number of characters in word
        :Auxiliary space (worst case): O(q) where q is the number of characters in word
        :param letter_ind: The character index of word to indicate the character to search for in the trie
        :param word: Contains the string that is being searched for within this traversal
        :param wordlen: The number of characters in word
        :return: The number of words added to the trie that the query is a prefix of
        """

        # Traversing through all letters in the query will mean the last node stores the counter of prefix occurrence
        if letter_ind == wordlen:
            return self.prefixfreq

        # If the prefix does not exist in the trie
        elif self.letter != word[letter_ind]:
            return 0

        return self.children[(ord(word[letter_ind+1]) - 97) % 26].prefix_exists(letter_ind + 1, word, wordlen)

    def wildcard_found(self, strings_split, wild_cards):
        """
        This function is used when a "?" character is found in strings_split[0], it acts as a bridge to keep
        traversing the trie by each character, but makes sure it traverses from every possible character ?
        can represent. If "?" represents the end of the wildcard prefix, it will instead stop traversing through
        the prefix and instead find all possible words in text that the wildcard prefix is a prefix of.

        :Time complexity (worst case): O(q + S) where q is the number of characters in string_split[1] and
        S is the number of nodes which are part of the sub tree of the current node
        :Auxiliary space (worst case): O(S + W) where S is the maximum depth of the sub trie
        and number of parent nodes, and W is the number of elements in wild_cards
        :param strings_split: A list with one element containing the wildcard prefix characters before and
        including the '?', and the other element containing characters of the wildcard prefix after the '?'
        :param wild_cards: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        :return: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        """

        # This is called if "?" is the last character of the query, jumps straight to all wildcards
        if strings_split[1] == "" and self.letter is not None:
            if self.word is not None:
                for i in range(self.wordfreq):
                    wild_cards.append(self.word)
            if self.haschild:
                for i in range(26):
                    wild_cards = self.children[i].all_wildcards(wild_cards)
            return wild_cards

        # Gets new length of characters after "?" in query
        string_len = len(strings_split[1]) - 1

        # No node value means no children, no need to further traverse
        if self.letter is None:
            return wild_cards

        return self.children[(ord(strings_split[1][0]) - 97) % 26] \
            .wildcard_exists_second(0, strings_split, string_len, wild_cards)

    def wildcard_exists_first(self, letter_ind, strings_split, string_len, wild_cards):
        """
        Traverses across all characters in strings_split[0] in the trie, when it reaches the last character of
        strings_split[0], which will always be a "?", it will call wildcard_found in all child nodes to continue
        the traversal in the trie.

        :Time complexity (worst case): O(q + S) where q is the number of characters in query_str and
        S is the total number of all characters across all strings in text
        :Auxiliary space (worst case): O(S + W) where S is the maximum depth of the sub trie
        and number of parent nodes, and W is the number of elements in wild_cards
        :param letter_ind: The character index of strings_split[0] to indicate the character to search for in the trie
        :param strings_split: A list with one element containing the wildcard prefix characters before and
        including the '?', and the other element containing characters of the wildcard prefix after the '?'
        :param string_len: The number of characters in strings_split[0]
        :param wild_cards: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        :return: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        """

        # Reached the "?", time to call wildcard_found function to further traverse the trie
        if letter_ind == string_len-1:
            if self.letter is not None:
                if self.haschild:
                    for wildcard_letter in range(26):
                        wild_cards = self.children[wildcard_letter].wildcard_found(strings_split, wild_cards)

            return wild_cards

        # No such wildcard prefix
        elif self.letter != strings_split[0][letter_ind]:
            return wild_cards

        return self.children[(ord(strings_split[0][letter_ind+1]) - 97) % 26]\
            .wildcard_exists_first(letter_ind + 1, strings_split, string_len, wild_cards)

    def wildcard_exists_second(self, letter_ind, strings_split, string_len, wild_cards):
        """
        Traverses across all characters in strings_split[1] in the trie. After it reaches the end of this string,
        all child nodes will contain the words in text that the string represented by both elements of strings_split
        is a wildcard prefix of.

        :Time complexity (worst case): O(q + S) where q is the number of characters in string_split[1] and
        S is the number of nodes which are part of the sub tree of the current node
        :Auxiliary space (worst case): O(S + W) where S is the maximum depth of the sub trie
        and number of parent nodes, and W is the number of elements in wild_cards
        :param letter_ind: The character index of strings_split[1] to indicate the character to search for in the trie
        :param strings_split: A list with one element containing the wildcard prefix characters before and
        including the '?', and the other element containing characters of the wildcard prefix after the '?'
        :param string_len: The number of characters in strings_split[1]
        :param wild_cards: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        :return: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        """

        # Reached the end of the wildcard prefix, time to call all_wildcards function to get all words in text
        if letter_ind == string_len:
            if self.word is not None:
                for i in range(self.wordfreq):
                    wild_cards.append(self.word)
            if self.letter is not None and self.haschild:
                for i in range(26):
                    wild_cards = self.children[i].all_wildcards(wild_cards)

            return wild_cards

        # No such prefix
        elif self.letter is None:
            return wild_cards

        return self.children[(ord(strings_split[1][letter_ind+1]) - 97) % 26]\
            .wildcard_exists_second(letter_ind + 1, strings_split, string_len, wild_cards)

    def all_wildcards(self, wild_cards):
        """
        This function is called when its fully traversed through all characters of the wildcard prefix in the trie,
        it will add all words the nodes which are children of the node representing the last character of the wildcard
        prefix are representing to the list wild_cards.

        :Time complexity (worst case): O(S) where S is the number of all child nodes of the current node
        :Auxiliary space (worst case): O(S + W) where S is the maximum depth of the sub trie
        and number of parent nodes, and W is the number of elements in wild_cards
        :param wild_cards: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        :return: A list of all the strings found which is a wildcard prefix of the string strings_split
        represents (two string elements of strings_split combined make the entire string)
        """

        # Found a word! This is a valid word, put it in our collection of wildcards self.wordfreq no of times
        if self.word is not None:
            for i in range(self.wordfreq):
                wild_cards.append(self.word)

        # If node has children, these will be valid words as well, find them if true
        if self.letter is not None and self.haschild:
            for i in range(26):
                wild_cards = self.children[i].all_wildcards(wild_cards)

        return wild_cards

#trie = Trie([])
trie = Trie(["aa","aab","aaab","abaa","aa","abba","aaba","aaa","aa","aaab","abbb","baaa","baa","bba","bbab", "abba"])
#trie = Trie(["aaab"])
#print(trie.string_freq("aa"))
#trie = Trie(["james", "jakes", "tom", "tamm"])
#print(trie.letters())
#print(trie.prefix_freq("aab"))
#trie = Trie([])
#trie = Trie(["my", "name", "is","bronwyn","madama","my","ym","james","m"])
print(trie.wildcard_prefix_freq("a?a"))
#print(trie.prefix_freq("aa"))
