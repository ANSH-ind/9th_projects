#include <iostream>
#include <fstream>
#include <string>
#include <limits>
#include <sstream>

using namespace std;

int getlastroll() {
    ifstream studentdata("studentdatas.txt");
    string line;
    int lastroll = 0;

    if (studentdata.is_open()) {
        while (getline(studentdata, line)) {
            if (line.empty()) continue; // Khali lines ko skip karein

            stringstream ss(line);
            int currentroll;
            if (ss >> currentroll) {
                lastroll = currentroll; // Har line ka pehla number roll number hoga
            }
        }
        studentdata.close();
    }
    return lastroll;
}

void addstudent() {
    string name;
    int classnumber;
    int rollnumber = getlastroll() + 1;

    cout << "Enter student name: ";
    getline(cin, name);

    cout << "Enter class: ";
    cin >> classnumber;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    ofstream studentsdata("studentdatas.txt", ios::app);
    if (studentsdata.is_open()) {
        // Naam mein space ho sakti hai, isliye format ka dhyan rakhein
        studentsdata << rollnumber << " " << name << " " << classnumber << "\n";
        cout << "Student added successfully. Roll Number: " << rollnumber << "\n";
        studentsdata.close();
    }
}

int main() {
    string command;
    while (true) {
        cout << "COMMAND (add_student / exit): ";
        getline(cin, command);
        if (command == "exit") {
            break;
        }
        else if (command == "add_student") {
            addstudent();
        }
    }
    return 0;
}
