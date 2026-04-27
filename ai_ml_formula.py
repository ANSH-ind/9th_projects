#by ansh raj a ai ml learner
#first me import math module to perform some calclution
import math
#implement this cosin similarity formula (cosin(A,B)=A•B/|A|*|B|) in the function
def cosin_similarity(A,B):
	#find the dot product of 'A' and 'B'
	#here we use for loop and zip to extract the values from 'A' and 'B' and then multiply by a*b and calclute total sum
	dot = sum(a*b for a,b in zip(A,B))
	#now find magnitude by using formula mag = √sum(a1*a1,a2*a2...)
	mag_A = math.sqrt(sum(a for a in A))
	mag_B = math.sqrt(sum(b for b in B))
	#return dot/(magnitude_of_A×magnitude_of_B)
	return dot/(mag_A*mag_B)
	
#now check by an example
#take two array or np.array
print("COSIN SIMILARITY")
a = [1,2,3,4]
b = [1,2,3,4]
print(f"examole 'a'--> {a}")
print(f"examole 'b'--> {b}")
print(f"output : {cosin_similarity(a,b)}")
#output become 2.9999999999999996


#now we are going to implement ReLU activaction function from scratch 

#define formula relu(x) = max(0,x)
def ReLU(x):
	#return max(0,x) so when input is grater than 0 it return x but when x < 0 it return maximum value called 0
	return max(0,x)
#check our formula and function by examples
x = 5
y = -2
print(f"example x--> {x}")
print(f"example y--> {y}")
print(f"the number {x} is grater than 0 so it become unchanged {ReLU(x)}\nand {y} is less than 0 so it become 0 output : {ReLU(y)}")

#output : the number 5 is grater than 0 so it become unchanged 5 and -2 is less than 0 so it become 0 output : 0

#let's implement sigmoid
#we know that the formula of sigmoid is sigma(x) 1/1+e^(-x)
def sigmoid(x):
	return 1/(1+math.exp(-x))
#check using examples
a = 2
b = -2
print(f"examaple a --> {a}")
print(f"examaple b --> {b}")
print(f"{a} after sigmoid {sigmoid(a)}\nb after sigmoid {sigmoid(b)}")

#we are going to create softmax 
#we know the formula of softmax softmax(x)= (e^x-max(x))/(sum(e^x-max(x)))
#important notice this done on an array or tensor
def softmax(x_list):
	#find the maxmium value from arrya 
	max_value = max(x_list)
	#now find exponintial values of numbers that are in array using loop
	exp_values = [math.exp(x-max_value) for x in x_list]
	#now calclute total of exp_valuea
	total = sum(exp_values)
	#return a list [val/total for val in exp_values]
	return [val/total for val in exp_values]

#now check our defined function by an array

array = [1,2,3,4,8]
print(f"examaple array --> {array}")
result = softmax(array)
print([f'{x:.2f}' for x in result])
#and the total sum of result become 100
print(f"the sum is {sum(result)*100}%")
print("thanks bro")
