#include <iostream>
#include <fstream>
#include <string>
#include <limits>

using namespace std;

int getlastroll(){
  ifstream studentdata("studentdatas.txt");
  int currentroll,classnumber;
  string name;
  int lastroll = 0;
  if(studentdata.is_open()){
    while(studentdata>>currentroll>>name>>classnumber){
      lastroll = currentroll;
    }
    studentdata.close();
  }
  return lastroll;
}

void addstudent(){
  string name;
  int classnumber;
  int rollnumber = getlastroll()+1;
  cout<<"enter student name :";
  getline(cin,name);
  cout<<"enter class :";
  cin>>classnumber;
  cin.ignore(numeric_limits<streamsize>::max(),'\n');
  ofstream studentsdata("studentdatas.txt",ios::app);
  if(studentsdata.is_open()){
    studentsdata<<rollnumber<<" "<<name<<" "<<classnumber<<"\n";
    cout<<"student added successfully"<<"\n";
    studentsdata.close();
  }
}

int main(){
  string command;
  while(true){
    cout<<"COMMAND : ";
    getline(cin, command);
    if(command=="exit"){
      break;
    }
    else if(command=="add_student"){
      addstudent();
    }
  }
  return 0;
}
