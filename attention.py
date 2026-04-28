#we are going to define softmax function and attention is all you need from scratch using math module in python
#first of all i say you that "attention is all you need" is comming from google research 


#now import math module 
import math
#now define our softmax function to use in the attention function.
def softmax(array): #this take a array or vector and pass forward.
    #find maxmium value of the array then subtract by all number that are in array using loop 
    max_val = max(array)
    #find exponintal value of (x-maximuim value of array) using loop
    #we now that the exponintal value ids aprox 2.71... but here we using built in exp function of math
    exp_val = [math.exp(x - max_val) for x in array]
    #now calclute the total sum of exponintal value 
    total = sum(exp_val)
    #return all number that are in exponintal value one by one/total 
    return [val / total for val in exp_val]

#now we are going to define attention is all you need 
#here we take Q,K,V means Q = query , K = key and V = value 
"""
what means query, key and value?

query --> what we search.

key --> what is the main focuse of our sentance. for example : "what do the dog" here do reletes to dog

value --> what is the real value of the queary.
"""
def attention(Q, K, V):
    #find dimenson of K 

#here i write len(K[0]) that means 
#let = 
#K = [[1,2,3],
#[1,0,1]]
#we call K[0] to get the index of [1,2,3] but i want lenght of that index so we call len(K[0])
 
    d_k = len(K[0])
    #create a empity list 
    scores = []
    #using loop we extract the number that are in Q and K matrix and then find the dot product of Q and K       
    for q in Q:
        #create a empity list to store the simalirity of Q and K
        row = []
        for k in K:
            #here we use zip to avoide loop
            dot = sum(dq * dk for dq, dk in zip(q, k))
            #now store similarity after finding dot product 
            row.append(dot / math.sqrt(d_k))
            """
            here is a question why we store row in score?
            the answer is to create vector to matrix form
            """
        scores.append(row)
    #now we use use our softmax function to find weights of the attention by using loop 
    attention_weight = [softmax(row) for row in scores]
    #create empity list to store the new_row in the form of matrix
    
    output = []
    #extract all number that are in attention weight 
    for weights in attention_weight:
        #create a empity list store value that are comes from sum of weight and V(value) 
        new_row = []
        #here we find lenght of V(value)[0] means the index 0th of V
        for i in range(len(V[0])):
            #using loop we multiply the elements of weight[j] from V[j][i] and store in the new_now list
            value = sum(weights[j] * V[j][i] for j in range(len(V)))
            new_row.append(value)
        output.append(new_row)
    #now return output and attention weights 
    return output, attention_weight

#lets check our cook 
Q = [[1, 0]]

K = [
    [1, 0],
    [0, 1]
]

V = [
    [10, 0],
    [0, 20]
]

print(f"the attention is : \n{attention(Q, K, V)}")
#the output attention is :
#([[6.697615493266569, 6.604769013466862]], [[0.6697615493266569, 0.3302384506733431]])
