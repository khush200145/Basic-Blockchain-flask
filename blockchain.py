import datetime
import hashlib
import json
from flask import Flask, jsonify

#PART-1- Building Blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.coin_value=0
        self.create_block(proof=1,previous_hash='0')
    
        
    def create_block(self,proof,previous_hash):
    
        self.coin_value+=1
        block={'index':len(self.chain),'proof':proof,'timestamp':str(datetime.datetime.now()),'previous_hash':previous_hash,'coin_value':self.coin_value}
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2- previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    
    

    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while(block_index<len(chain)):
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2- previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block=block
            block_index+=1
        return True
    #PART-2 Mining our blockchain
    #Creating a web app
app=Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=False
app.config['JSON_SORT_KEYS'] = False
#creating a blockchain
blockchain=Blockchain()
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash)
    response={'message':'Congats! You have successfulkly mined a block','index':block['index'],'timestamp':block['timestamp'],'proof':block['proof'],'previous_hash':block['previous_hash']}
    return jsonify(response),200
@app.route('/get_chain',methods=['GET'])
def get_chain():
    
    previous_block_mined=blockchain.get_previous_block()
    response={'blockchain':blockchain.chain,'length':len(blockchain.chain),'Last Block mined time':previous_block_mined['timestamp']}
    return jsonify(response),200
@app.route('/is_valid',methods=['GET'])
def is_valid():
    blockchain.coin_value-=1
    
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={'message':'Congrats!The Blockchain is valid.Keep it up',
                  'Coin Value decreased to->':blockchain.coin_value}
        return jsonify(response),200
    else:
        response={'message':'OOPS! Houston we got a problem'}
        return jsonify(response),200
@app.route('/get_chain_length', methods=['GET'])
def get_chain_length():
    response={'blockchain length':len(blockchain.chain)}
    return jsonify(response),200
#RUNNING THE APP
app.run(host='0.0.0.0',port=5000)

@app.route ('/get me_current_coin_value',methods=['GET']) 
def get_me_current_coin_value():
    response={'Current value of coin is->': blockchain.coin_value}
    return jsonify(response),200


       
    
    
       
        
        
        
    
    
    
            
            
        
            

