#include <iostream>
#include <cmath>
using namespace std;

void is_equilateral(){
    float A[2], B[2], C[2];

    cout<<"Enter x1 y1: ";
    cin>>A[0]>>A[1];

    cout<<"Enter x2 y2: ";
    cin>>B[0]>>B[1];

    cout<<"Enter x3 y3: ";
    cin>>C[0]>>C[1];

    float AB = sqrt(pow(A[0]-B[0],2) + pow(A[1]-B[1],2));
    float BC = sqrt(pow(B[0]-C[0],2) + pow(B[1]-C[1],2));
    float CA = sqrt(pow(C[0]-A[0],2) + pow(C[1]-A[1],2));

    if(abs(AB-BC) < 0.0001 && abs(BC-CA) < 0.0001){
        cout<<"This is an equilateral triangle\n";
    } else {
        cout<<"This is NOT an equilateral triangle\n";
    }
}

int main(){
    string command;
    bool terminal = true;

    while(terminal){
        cout<<"Enter command (solve/exit): ";
        cin>>command;

        if(command=="solve"){
            is_equilateral();
        }
        else if(command=="exit"){
            terminal = false;
        }
        else{
            cout<<"Enter correct command\n";
        }
    }
    return 0;
}
