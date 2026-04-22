#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <limits>
#include <algorithm>
#include <vector>

using namespace std;

struct Student {
    int roll;
    string name;
    int classnum;
};

int getLastRoll() {
    ifstream file("studentdatas.txt");
    string line;
    int lastroll = 0;
    while (getline(file, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        string temp;
        getline(ss, temp, ',');
        if (!temp.empty()) lastroll = stoi(temp);
    }
    file.close();
    return lastroll;
}

void addStudent() {
    ofstream file("studentdatas.txt", ios::app);
    int roll = getLastRoll() + 1;
    string name;
    int classnum;

    cout << "ENTER CLASS: ";
    cin >> classnum;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "ENTER STUDENT NAME: ";
    getline(cin, name);

    file << roll << "," << name << "," << classnum << "\n";
    file.close();
    cout << "\nSTUDENT ADDED - ROLL NO: " << roll << endl;
}

void searchStudent() {
    ifstream file("studentdatas.txt");
    if (!file.is_open()) {
        cout << "File not found!" << endl;
        return;
    }

    vector<Student> studentList;
    string line;

    while (getline(file, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        string r_str, n_str, c_str;
        getline(ss, r_str, ',');
        getline(ss, n_str, ',');
        getline(ss, c_str, ',');

        if (!r_str.empty()) {
            Student s;
            s.roll = stoi(r_str);
            s.name = n_str;
            s.classnum = stoi(c_str);
            studentList.push_back(s);
        }
    }
    file.close();

    vector<int> rolls;
    for (const auto& s : studentList) {
        rolls.push_back(s.roll);
    }

    int target;
    cout << "ENTER ROLL NUMBER TO SEARCH: ";
    cin >> target;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    auto start = rolls.begin();
    auto end = rolls.end();
    auto it = lower_bound(start, end, target);

    if (it != end && *it == target) {
        int index = it - start;
        cout << "\n--- STUDENT FOUND ---" << endl;
        cout << "ROLL NO : " << studentList[index].roll << endl;
        cout << "NAME    : " << studentList[index].name << endl;
        cout << "CLASS   : " << studentList[index].classnum << endl;
    } else {
        cout << "Student not found!" << endl;
    }
}

int main() {
    string choice;
    while (true) {
        cout<<"use this command";
        cout << "\n1. add_student\n2. search_student\n3. exit\ncommand : ";
        getline(cin, choice);

        if (choice == "exit()" || choice == "exit") {
            break;
        } else if (choice == "add_student" || choice == "add") {
            addStudent();
        } else if (choice == "search student" || choice == "search") {
            searchStudent();
        } else {
            cout << "Invalid choice!" << endl;
        }
    }
    return 0;
}
