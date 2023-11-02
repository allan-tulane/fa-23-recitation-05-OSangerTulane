import math, queue
from collections import Counter

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    ## This function is done.
    ## Given any file name, this function reads line by line to count the frequency per character. 
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        x = p.get()
        y = p.get()
        z = TreeNode(left=x, right=y, data=(x.data[0] + y.data[0], ""))
        p.put(z)
        
    # return root of the tree
    return p.get()

# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code={}):
  if node is not None:
      if node.data[1] != "":
          code[node.data[1]] = prefix
      get_code(node.left, prefix + "0", code)
      get_code(node.right, prefix + "1", code)
  return code

# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
  alphabet_size = len(f)
  total_chars = sum(f.values())
  return alphabet_size * math.ceil(math.log2(total_chars))

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
  total_cost = 0
  for char, freq in f.items():
      total_cost += len(C[char]) * freq
  return total_cost

text_files = ['alice29.txt', 'asyoulik.txt', 'f1.txt', 'fields.c', 'grammar.lsp']

print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("File", "Alphabet Size", "Fixed Length", "Huffman Cost", "Ratio (Huffman/Fixed)"))
for file in text_files:
    f = get_frequencies(file)
    alphabet_size = len(f)
    fixed_len_cost = fixed_length_cost(f)
    T = make_huffman_tree(f)
    C = get_code(T)
    huffman_cost_value = huffman_cost(C, f)
    ratio = huffman_cost_value / fixed_len_cost
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(file, alphabet_size, fixed_len_cost, huffman_cost_value, ratio))

# Calculate the expected cost of a Huffman encoding for the same frequency for each character
equal_frequency = {'A': 10, 'B': 10, 'C': 10, 'D': 10, 'E': 10}
T_equal = make_huffman_tree(equal_frequency)
C_equal = get_code(T_equal)
huffman_cost_equal = huffman_cost(C_equal, equal_frequency)
print("Expected Huffman Cost for Equal Frequencies: %d" % huffman_cost_equal)


