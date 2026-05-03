#include <iostream>
#include <cmath>
using namespace std;
int main(){
	cout<<"QUESTION: \nshow that the points A(3,0),B(6,4) and C(-1,3) are the vertices of an isosceles right traingle."<<endl;
	float A[2] = {3,0};
	float B[2] = {6,4};
	float C[2] = {-1,3};
	//assign all the A,B and C points to x and y
	float x1 = A[0];
	float y1 = A[1];
	float x2 = B[0];
	float y2 = B[1];
	float x3 = C[0];
	float y3 = C[1];
	//now find the distance between all the three points and then check if two points are matching then we say that this is an isosceles trangle 
	cout<<"\nSOLUTION-->\n";
	cout<<"find the distance using pythagoras therom (√(x1-x2)^2+(y1-y2)^2)\n";
	float AB = sqrt(pow(x1-x2,2)+pow(y1-y2,2));
	cout<<"\ndistance between A and B is: "<< AB<<endl;
	float BC = sqrt(pow(x2-x3,2)+pow(y2-y3,2));
	cout<<"\ndistance between B and C is: "<<BC<<endl;
	float CA = sqrt(pow(x3-x1,2)+pow(y3-y1,2));
	cout<<"\ndistance between C and A is : "<<CA<<"\n";
	if(AB==BC or BC==CA or CA==AB){
		cout<<"\nthis is an isosceles trangle\n";
	}
	else{
		cout<<"\nthis is not an isosceles trangle";
	}
	return 0;
}
	
