import hashlib
from datetime import datetime

studentNames = ["Wong Kin Seong", "Chua Boon Kiat", "Alex Toh Jun Rong", "Wilson Neo Wei Feng"]
blockArr = []  # list which is used to store each Block object
currentTime = datetime.now().strftime("%H:%M %d/%m/%Y")


# Class to create the block for the blockchain
class Block:

    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = str(timestamp)
        self.data = data

        self.textToHash = data + timestamp + str(index)  # concatenate the student name,timestamp and index for hashing

        self.hash = calculateHash(self.textToHash)  # turns the hash value into a string


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
        b = Block(i, 0, currentTime, studentNames[i])  # if first block, make previousHash = 0
    else:
        b = Block(i, blockArr[i - 1].hash, currentTime, studentNames[i])

    blockArr.append(b)  # append the generated block object into the blockArr array
