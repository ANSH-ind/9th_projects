import math
"""
today we are going to solve a question.

show that the points A(3,0),B(6,4) and 
C(-1,3) are the vertices of an isosceles right traingle.

"""
"""
sol --> we know that the right isosceles triangle have 180° and one side are 90° called hypo... and 2 sides are equal they are 1. base 45° 
2. perpen... 
45° 
so b^2+p^2 = h^2 
"""
A = [3,0]
B = [6,4]
C = [-1,3]
#first of all we find the distance of all points AB,BC,CA
x1,y1 = A[0],A[1]
x2,y2 = B[0],B[1]
AB = math.sqrt(((x1-x2)**2)+((y1-y2)**2))
print(f"distance of AB is {AB}")

#now find point BC 
#here we use same index of B that use before this

cx1,cy1 = C[0],C[1]
#now use pythagoras therom to find distance
BC = math.sqrt(((x2-cx1)**2)+((y2-cy1)**2))
print(f"distance of BC is {BC}")

#find CA and here we also use same index that are use to find distance AB and BC

CA = math.sqrt(((cx1-x1)**2)+((cy1-y1)**2))
print(f"distance of CA is {CA}")

#check which line are same and which are diffrance 

print(f"checking AB is equal to BC {AB==BC}")
print(f"checking BC is equal to CA {BC==CA}")
print(f"checking CA is equal to AB {CA==AB}")
#so CA is equal to AB now we know that two side equal in isosceles right traingle that are CA==AB 

