print("EXAMPLE")
import math
A = [2,4]
B = [2,6]
C = [2+math.sqrt(3),5]

#now find the distance between point A , B and C using pythogaras therom
x1,y1 = A[0],A[1]
x2,y2 = B[0],B[1]

#put this values in pythagoras therom 

AB = math.sqrt(((x1-y1)**2)+((x2-y2)**2))
print(f"the disctane between A an B is {AB}")

z1,a1 = C[0],C[1]

BC = math.sqrt(((x2-z1)**2)+((y2-a1)**2))
print(f"\nthe distance between B and C is {BC}")

CA = math.sqrt(((z1-x1)**2)+((a1-y1)**2))
print(f"\nthe distance between C and A is {CA}")

#to prove that AB, BC and CA is to make a equilateral traingle wahre all like mete togeather and make quilateral.
print(f"\nAB is equal to BC : {AB==BC}")
print(f"\nBC is equal to CA : {BC==CA}")
print(f"\nCA is equal to AB : {CA==AB}")
#we now that in equilateral triangle all sides are equal and sum of all angle is 180° but her one side not match so this is not a equlitral triangle 
#if you want to try this with your question run this code in your python ide like pydroid available on playstore 
def is_equilateral(A,B,C):
	x1,y1 = A[0],A[1]
	x2,y2 = B[0],B[1]
	x3,y3 = C[0],C[1]
	
	AB = math.sqrt(((x1-y1)**2)+((x2-y2)**2))
	print(f"\nthe distance between A and B is : {AB}")
	
	BC = math.sqrt(((x2-x3)**2)+((y2-y3)**2))
	print(f"\nthe distance between B and C	is : {BC}")
	
	CA = math.sqrt(((x3-x1)**2)+((y3-y1)**2))
	print(f"\nand the last distance between C and A is : {CA}")
	
	if AB==BC and BC==CA and CA==AC:
		return f"\nyour triangle is an equilateral triangle\ndistance between them are\nA to B {AB} , B to C  : {BC} and C to A is : {CA}"
	else:
		return "\nthis is not a equilateral triangle because there all side doesn't match or equal"
		
print("\nnow try this with your yourself")
terminal = True
while terminal:
	command = input("\nenter (solve) to solve cordinate geomitary probelem :")
	if command == "solve":
		A = list(map(int, input("\nenter X1 and Y1 of A point : ").split()))
		B = list(map(int, input("\nenter X2 and Y2 of B point : ").split()))
		C = list(map(int, input("\nenter X3 and Y3 of C point : ").split()))
		print(f"{is_equilateral(A,B,C)}")
	elif command != "solve" or "exit" or "EXIT":
		print("\nyou enter wrong command")
	elif command == "exit" or "EXIT":
		terminal = False 
	


