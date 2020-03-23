import copy
import hashlib
from datetime import datetime

studentNames = ["Wong Kin Seong", "Koh Boon Kiat", "Alex Toh Jun Rong", "Wilson Neo Wei Feng"]
blockArr = []  # list which is used to store each Block object
currentTime = datetime.now().strftime("%H:%M %d/%m/%Y")


# Class to create the block for the blockchain
class Block:
    # Constructor for block to take in parameters
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data
        self.previous_hash = previous_hash
        self.text_to_hash = data + timestamp + str(index)  # concatenate the student name,timestamp and index for hashing
        self.hash = calculatehash(self.text_to_hash)  # turns the hash value into a string

    # Function is used to convert the input into a sha-256 hash
def calculatehash(text):
    m = hashlib.sha256()  # sha256 is used for the hashing
    m.update(text.encode('utf-8'))
    return m.hexdigest()  # turns the hash value into a string

#
# # For loop to create block objects for the different student names
# for i in range(len(studentNames)):
#     if i == 0:
#         b = Block(i, currentTime, studentNames[i], 0)  # if first block, make previousHash = 0
#     else:
#         b = Block(i, currentTime, studentNames[i], blockArr[i - 1].hash)
#
#     blockArr.append(b)  # append the generated block object into the blockArr array
#












