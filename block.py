import hashlib

# Class to create the block for the blockchain
class Block:
    # Constructor for block to take in parameters
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # concatenate the student name,timestamp and index for hashing
        self.text_to_hash = data + timestamp + str(index) + previous_hash
        # turns the hash value into a string
        self.hash = calculatehash(self.text_to_hash)


# Function is used to convert the input into a sha-256 hash
def calculatehash(text):
    m = hashlib.sha256()  # sha256 is used for the hashing
    m.update(text.encode('utf-8'))
    return m.hexdigest()  # turns the hash value into a string













