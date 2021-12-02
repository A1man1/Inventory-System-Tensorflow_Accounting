class TrieNode:
 
    def __init__(self, char,dict_data=None):
 
        self.char = char
 
        self.is_end = False
 
        self.children = {}

        self.dict_data=None
 
class Trie(object):
 
    def __init__(self):
 
        self.root = TrieNode("",{})
     
    def insert(self, word,dict_data=None):
 
        node = self.root
 
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
 
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
         
        node.is_end = True
        node.dict_data=dict_data
         
    def _dfs(self, node, pre):
 
        if node.is_end:
            self.output.append({'result':(pre + node.char),'data':node.dict_data})
         
        for child in node.children.values():
            self.dfs(child, pre + node.char)
         
    def search(self, x):
        
        node = self.root
         
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
               
                return []
         
        self.output = []
        self._dfs(node, x[:-1])
 
        return self.output