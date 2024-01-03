string = '<6736,3.66,-4.23,8.06,7.50,-5.00,0.00,-15.00,43.69,1.06,359.69,22.69,28.44><6756,3.73,-4.27,7.94,7.06,-7.13,-0.25,-15.00,43.69,1.06,359.63,22.75,28.31>'

# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)
    

def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

freq = {}
for c in string:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1
freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])



def huffman_encode(string):
    output = ""
    for char in string:
        output += huffmanCode[char]
    return output

def huffman_decode(string):
    output = ""
    code = ""
    for char in string:
        code += char
        for k in huffmanCode:
            if huffmanCode[k] == code:
                output += k
                code = ""
                break
    return output

def convert2binary(string):
    output = ""
    for char in string:
        output += bin(ord(char))[2:].zfill(8)
    return output

#str = "123.12"
#encoded = huffman_encode(str)
#print(encoded)
#print the length of the encoded string and the length of the binary string
#print(huffman_decode(encoded))



