from block import *
import datetime


# Block chain synchronisation (Creation of the block chain)
class BlockChain:
    def __init__(self):
        self.blocks = [self.getgenesisblock()]

    # Creation of genesis/root block
    def getgenesisblock(self):
        return Block(index=0, timestamp="00:00 20/3/2020", data="ICT1010", previous_hash="0")

    # Generate new block and add to chain
    def addblock(self, data):
        timestamp = str(datetime.now().strftime("%H:%M %d/%m/%Y"))
        new_block = Block(index=len(self.blocks), timestamp=timestamp,
                          data=data, previous_hash=self.blocks[len(self.blocks) - 1].hash)
        if self.isvalidnewblock(new_block=new_block,prev_block=self.blocks[len(self.blocks)-1]):
            self.blocks.append(new_block)
        else:
            print("Unable to add block to chain")

    # Return size of current chain
    def length(self):
        return len(self.blocks)

    # Verify each block integrity in block chain
    def verify(self, verbose):
        """verbose = True to print error message"""
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print("Wrong index at block {i}")

            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                flag = False
                if verbose:
                    print("Wrong previous hash at block {i}")
            if self.blocks[i].hash != calculatehash(self.blocks[i].text_to_hash):
                flag = False
                if verbose:
                    print("Wrong hash at block {i}")

            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print("Backdating at block {i}")

            return flag

    # Check the validity of the generated block
    def isvalidnewblock(self, new_block, prev_block):
        if prev_block.index + 1 != new_block.index:
            print("Invalid Index")
            return False
        elif prev_block.hash != new_block.previous_hash:
            print("Invalid PreviousHash")
            return False
        elif calculatehash(new_block.text_to_hash) != new_block.hash:
            print("Hash Value invalid")
            return False
        return True

    # Replace current block chain with new block chain if old length < new length
    def replacechain(self,new_chain):
        if new_chain.verify(verbose=False) and new_chain.length() > self.length():
            self.blocks = new_chain
            print("Replaced current chain")
        else:
            print("Unable to replace chain")
