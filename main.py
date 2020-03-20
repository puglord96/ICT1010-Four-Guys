import hashlib

index = 0
studentNames = {"Wong Kin Seong","Chua Boon Kiat","Alex Toh Jun Rong","Wilson Neo Wei Feng"}

class Block:

    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data

        m = hashlib.sha256()
        m.update(data.encode('utf-8'))
        self.hash = m.hexdigest()


for i in range(len(studentNames)):
    print("joi")


