#we are going to implement backpropogation in python from scratch 

import math
#set up input and true label 
x = 2.0
y_truth = 10.0

#set wight,bise and learning rate
w = 0.5
b = 1.0
lr = 0.01
#forward pass
for i in range(100):
	#di forward pass
	y_pred = w*x+b
	# calculate the loss
	loss = (y_pred-y_truth)**2
	#find darivatives of loss respect to y_pred
	dl_dy = 2*(y_pred-y_truth)
	#darivatives of weight respect to loss
	dl_dw = dl_dy*x
	#darivatives of bise respect to loss
	dl_db = dl_dy*1
	#change weight and bise
	w = w-lr*dl_dw
	b = w-lr*dl_db
	if i% 20==0:
		print(f"epoch: {i} | loss: {loss:.4f}\nweight: {w} | bise: {b}")
prediction = w*x+b

print(f"prediction: {round(prediction)}")
