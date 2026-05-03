#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

int is_isosceles(){

    float x1, y1;
    float x2, y2;
    float x3, y3;

    cout<<"enter point x1: ";
    cin>>x1;
    cout<<"enter point y1: ";
    cin>>y1;

    cout<<"enter point x2: ";
    cin>>x2;
    cout<<"enter point y2: ";
    cin>>y2;

    cout<<"enter point x3: ";
    cin>>x3;
    cout<<"enter point y3: ";
    cin>>y3;

    float AB = sqrt(pow(x1-x2,2)+pow(y1-y2,2));
    float BC = sqrt(pow(x2-x3,2)+pow(y2-y3,2));
    float CA = sqrt(pow(x3-x1,2)+pow(y3-y1,2));

    float eps = 0.0001;

    if(fabs(AB-BC) < eps || fabs(BC-CA) < eps || fabs(CA-AB) < eps){
        cout<<"This is an isosceles triangle"<<endl;
    }
    else{
        cout<<"This is not an isosceles triangle"<<endl;
    }

    return 0;
}

int main(){
    bool terminal = true;

    while(terminal){
        string command;

        cout<<"\nenter command (is_isosceles/find/exit): ";
        getline(cin,command);

        if(command=="is_isosceles" || command=="find"){
            is_isosceles();
        }
        else if(command=="exit"){
            cout<<"Exiting math terminal..."<<endl;
            terminal = false;
        }
    }

    return 0;
}
