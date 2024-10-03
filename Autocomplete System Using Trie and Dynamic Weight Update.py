class TrieNode:
    def __init__(self):
        """
        Initialize a TrieNode with:
        - `children`: A dictionary to store references to child nodes.
        - `is_word`: A boolean flag indicating if this node marks the end of a valid word.
        - `weight`: The frequency or importance of the word ending at this node.
        """
        self.children = {}
        self.is_word = False
        self.weight = 0

class AutocompleteSystem:
    def __init__(self):
        """
        Initialize the Autocomplete system with a root TrieNode.
        """
        self.root = TrieNode()

    def insert(self, word, weight=1):
        """
        Insert a word into the Trie with an optional weight.
        - `word`: The word to insert.
        - `weight`: An optional argument representing the frequency or importance of the word (default is 1).
        """
        if not word:  # Edge case: Empty word
            return
        node = self.root
        for char in word:
            # If the character is not in the current node's children, add a new TrieNode for it
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True  # Mark the end of the word
        node.weight += weight  # Update the weight of the word

    def search_prefix(self, prefix):
        """
        Search for all words starting with the given prefix.
        - `prefix`: The prefix to search for.
        - Returns a list of (word, weight) tuples for all words that match the prefix.
        """
        node = self.root
        for char in prefix:
            # If the prefix character is not found in the Trie, return an empty list
            if char not in node.children:
                return []  # Edge case: Prefix not found
            node = node.children[char]
        # Once we reach the end of the prefix, find all words that follow it
        return self._find_words(node, prefix)

    def _find_words(self, node, prefix):
        """
        Helper function to recursively find all words starting from a given TrieNode.
        - `node`: The starting node.
        - `prefix`: The prefix built so far.
        - Returns a list of (word, weight) tuples.
        """
        results = []
        if node.is_word:
            # If the current node marks the end of a word, add it to the results
            results.append((prefix, node.weight))
        # Recursively find words in all child nodes
        for char, child_node in node.children.items():
            results.extend(self._find_words(child_node, prefix + char))
        return results

    def autocomplete(self, prefix):
        """
        Return autocomplete suggestions sorted by word weight (most frequent first).
        - `prefix`: The prefix to autocomplete.
        - Returns a list of (word, weight) tuples sorted by weight in descending order.
        """
        if not prefix:  # Edge case: Empty prefix
            return []
        # Find all words that match the prefix
        results = self.search_prefix(prefix)
        # Sort the results by weight in descending order
        return sorted(results, key=lambda x: -x[1])

# Test Cases
auto_system = AutocompleteSystem()

# Edge Case: Empty word insertion (should have no effect)
auto_system.insert("", 3)

# Inserting words with different weights
auto_system.insert("apple", 5)
auto_system.insert("app", 2)
auto_system.insert("application", 3)

# Test Case 1: Autocomplete with "app" (should return suggestions sorted by weight)
# Expected Output: [('apple', 5), ('application', 3), ('app', 2)]
print(auto_system.autocomplete("app"))

# Test Case 2: Autocomplete with empty prefix (edge case: returns empty list)
# Expected Output: []
print(auto_system.autocomplete(""))

# Test Case 3: Autocomplete with a non-existent prefix "xyz" (edge case: prefix not found)
# Expected Output: []
print(auto_system.autocomplete("xyz"))

# Test Case 4: Inserting another word with the same prefix "app"
auto_system.insert("appliance", 4)
# Expected Output: [('apple', 5), ('appliance', 4), ('application', 3), ('app', 2)]
print(auto_system.autocomplete("app"))

# Test Case 5: Autocomplete with a specific prefix "appli"
# Expected Output: [('application', 3), ('appliance', 4)]
print(auto_system.autocomplete("appli"))
