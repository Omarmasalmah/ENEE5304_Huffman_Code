# Importing libraries
import heapq
from collections import Counter
import math
import docx2txt

# Read the text file
def readText():
    text = docx2txt.process("To+Build+A+Fire+by+Jack+London.docx")
    return text
    

def buildFrequencyDict(text):
    frequencyDict = {}
    for char in text:
        #change to lower
        #char = char.lower()
        if char == ' ':
                # rename it
                    char = '(space)'
        if char != '\n':  # Skip newline characters
            if char not in frequencyDict:    
                frequencyDict[char] = 0
            frequencyDict[char] += 1
    return frequencyDict


# Calculate the total number of characters
def calculateTotalCharacters(frequencyDict):
    totalCharacters = 0
    for key, frequency in frequencyDict.items():
        totalCharacters += frequency
    return totalCharacters

# Calculate probabilitiies 
def calculateProbabilities(frequencyDict, totalCharacters):
    probabilitiesOfEachChar = {}
    # sort 
    frequencyDict = dict(sorted(frequencyDict.items(), key=lambda item: item[1], reverse=True))
    print("---------------------------------------------------------")
    print("{:<10} {:<12} {:<20}".format("Symbol", "Frequency", "Probability Of Char"))
    for key, frequency in frequencyDict.items():
        probabilitiesOfEachChar[key] = frequency / totalCharacters
    
        print(f"{key:<10} {frequencyDict[key]:<12} {probabilitiesOfEachChar[key]:.5f}")
    print("---------------------------------------------------------")

    return probabilitiesOfEachChar

# Calculate Entropy
def calculateEntropy(probabilitiesOfEachChar):
    entropy = 0
    for key, probability in probabilitiesOfEachChar.items():
        entropy += -probability * math.log(probability, 2)

    return entropy


#****------------------****************-------------*****************------------****************-----------***********
def buildHuffmanTree(frequency_dict):
    # Create a list of lists 
    heap = []
    for char, frequency in frequency_dict.items():
        # Add the frequency and the character to the list
        heap.append([frequency, [char, ""]])

    
    # Convert the list into a min-heap
    heapq.heapify(heap)
    
    # Continue merging nodes until there is only one node (Huffman tree)
    while len(heap) > 1:
        # Pop the two nodes with the lowest weights from the heap
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        
        # Add '0' as a prefix to the codewords of the low-weight node
        for pair in low[1:]:
            pair[1] = '0' + pair[1]
        
        # Add '1' as a prefix to the codewords of the high-weight node
        for pair in high[1:]:
            pair[1] = '1' + pair[1]
        
        # Merge the two nodes and push the result back into the heap
        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
    
    codewordsForTheCharacters = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    return codewordsForTheCharacters



#***************************************************************************************************************************************
# Build huffman tree in another way
class Node:
    def __init__(self, char=None, frequency=0, left=None, right=None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

def buildHuffmanTree2(frequency_dict):
    heap = []
    for c, frequency in frequency_dict.items():
        node = Node(char=c, frequency=frequency)
        heapq.heappush(heap, node)
    heapq.heapify(heap)
    
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        merged_node = Node(frequency=low.frequency + high.frequency, left=low, right=high)
        heapq.heappush(heap, merged_node)
    
    codewordsForTheCharacters = traverse_tree(heap[0])
    return codewordsForTheCharacters

def traverse_tree(node, code="", result=None):
    if result is None:
        result = []
    if node.char is not None:
        result.append((node.char, code))
    if node.left is not None:
        traverse_tree(node.left, code + "0", result)
    if node.right is not None:
        traverse_tree(node.right, code + "1", result)
    return sorted(result, key=lambda p: (len(p[1]), p))


#*****************************************************************************************************************************************************

# Find the average number of bits/character for the whole story using the Huffman code.
def findAverageNumberOfBits(codewords, probabilitiesOfEachChar):
    averageNumber = 0
    for char, codeword in codewords:
        averageNumber += probabilitiesOfEachChar[char] * len(codeword)
#    print("Average Number Of Bits For The Whole Story: ",averageNumber)
    return averageNumber


# Find the  percentage of compression accomplished by using the Huffman encoding as compared to ASCII code.
def findPercentageOfCompression(NASCII, Nhuffman):
    percentageOfCompression = (Nhuffman / NASCII) * 100
#    print("Percentage Of Compression: ",f"{percentageOfCompression: .2f}")
    return percentageOfCompression




# Main function
if __name__ == "__main__":
    text = readText()

    frequencyDict = buildFrequencyDict(text)
    totalCharacters = calculateTotalCharacters(frequencyDict)
    # Step -a- & -b-
    
    probabilitiesOfEachChar = calculateProbabilities(frequencyDict, totalCharacters)
    print("Total Characters: ",totalCharacters)

    # Step -c-
    entropy = calculateEntropy(probabilitiesOfEachChar)
    print("Entropy: ",f"{entropy: .5f} bits/character")

    # Step -1-
    codewords = buildHuffmanTree2(frequencyDict)
    
    # Step -3-
    # Average number of bits/character for the whole story using the Huffman code
    averageNumberOfBits = findAverageNumberOfBits(codewords, probabilitiesOfEachChar)
    print("Average: ",f"{averageNumberOfBits: .5f} bits/character")
    
    # Step -2-
    # Number of bits needed to encode the full story
    NASCII = totalCharacters * 8
    print("Number Of Bits For ASCII: ",NASCII)

    # Step -4-
    # Total number of bits needed to encode the entire story using Huffman code.
    Nhuffman = 0
    for char, codeword in codewords:
        Nhuffman += frequencyDict[char] * len(codeword)
    print("Number Of Bits For Huffman: ",Nhuffman)


    # Step -5-
    # Percentage of compression accomplished by using the Huffman encoding as compared to ASCII code.
    percentageOfCompression = findPercentageOfCompression(NASCII, Nhuffman)
    print("Percentage Of Compression: ",f"{percentageOfCompression: .2f}%")

    # Fill in the table to showcase some of your results, sorted as elphapet
    codewords.sort()  # Sort alphabetically based on the character
   
    print("-----------------------------------------------------------------")

    print("{:<10} {:<16} {:<18} {:<15}".format("Symbol", "Probability", "Codewords", "Length of codeword"))
    print("-----------------------------------------------------------------")
    for char, codeword in codewords:
        print(f" {char:<10} {probabilitiesOfEachChar[char]:.5f}         {codeword:<20} {len(codeword):<15}") 
        print("-----------------------------------------------------------------")
 
   
    #print table of a  b  c   d    e    f    m    z    space    .(dot)
    print("\n        Table to showcase some of the results")
    print("-----------------------------------------------------------------")
    print("{:<10} {:<15} {:<15} {:<15}".format(" Symbol", "Probability", "Codewords", "Length of codeword"))
    # Draw columns of | seperate

    for char, codeword in codewords:
        if char == 'a' or char == 'b' or char == 'c' or char == 'd' or char == 'e' or char == 'f' or char == 'm' or char == 'z' or char == '(space)' or char == '.':
            print("-----------------------------------------------------------------")
            print(f" {char:<10} {probabilitiesOfEachChar[char]:.5f}         {codeword:<17} {len(codeword):<15}")

    print("-----------------------------------------------------------------")

    