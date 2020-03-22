import copy
import hashlib
from datetime import datetime

studentNames = ["Wong Kin Seong", "Koh Boon Kiat", "Alex Toh Jun Rong", "Wilson Neo Wei Feng"]
blockArr = []  # list which is used to store each Block object
currentTime = datetime.now().strftime("%H:%M %d/%m/%Y")


# Class to create the block for the blockchain
class Block:

    def __init__(self, index, timestamp, data, previousHash):
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data
        self.previousHash = previousHash

        self.textToHash = data + timestamp + str(index)  # concatenate the student name,timestamp and index for hashing
        self.hash = calculateHash(self.textToHash)  # turns the hash value into a string

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.textToHash).encode('utf-8'))


# Function is used to convert the input into a sha-256 hash
def calculateHash(text):
    m = hashlib.sha256()  # sha256 is used for the hashing
    m.update(text.encode('utf-8'))
    return m.hexdigest()  # turns the hash value into a string


# Check the validity of the generated block
def isValidNewBlock(newBlock, prevBlock):
    if prevBlock.index + 1 != newBlock.index:
        print("Invalid Index")
        return False
    elif prevBlock.hash != newBlock.previousHash:
        print("Invalid PreviousHash")
        return False
    elif calculateHash(newBlock.textToHash) != newBlock.hash:
        print("Hash Value invalid")
        return False


# For loop to create block objects for the different student names
for i in range(len(studentNames)):
    if i == 0:
        b = Block(i, currentTime, studentNames[i], 0)  # if first block, make previousHash = 0
    else:
        b = Block(i, currentTime, studentNames[i], blockArr[i - 1].hash)

    blockArr.append(b)  # append the generated block object into the blockArr array


# blockchain synchronisation (Creation of the blockchain)
class minimalChain:
    def __init__(self):
        self.blocks = [self.getGenesisBlock()]

    # Creation of genesis block
    def getGenesisBlock(self):
        return Block(0, currentTime, studentNames[0], 0)

    def addBlock(self, data):
        self.blocks.append(Block(len(self.blocks), datetime.utcnow(), data,
                                 self.blocks[len(self.blocks) - 1].hash))

    def getChainSize(self):
        return len(self.blocks) - 1

    def verify(self, verbose):
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print("Wrong index at block {i}")

            if self.blocks[i - 1].hash != self.blocks[i].previousHash:
                flag = False
                if verbose:
                    print("Wrong previous hash at block {i}")
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                if verbose:
                    print("Wrong hash at block {i}")

            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print("Backdating at block {i}")

            return flag

    '''
    def fork(self, head='latest'):
        if head in ['latest', 'whole', 'all']:
            return copy.deepcopy(self)
        else:
            c = copy.deepcopy(self)
            c.blocks = c.blocks[0:head+1]
            return c

    def getRoot(self, chain_x):
        minChainSize = min(self.getChainSize(), chain_x.getChainSize())
        for i in range(1, minChainSize+1):
            if self.blocks[i] != chain_x.blocks[i]:
                return self.fork(i-1)

        return self.fork(minChainSize)

        '''












