#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>
using namespace std;

int main(int argc, char** argv) {

////////// DO NOT EDIT! //////////
  string path = argv[1];        //
//////////////////////////////////  
  
  //add code below this line

ifstream file(path);
string line;
string name;
string oldestName;
int age;
int maxAge = -1;

while (getline(file, line)) {
    stringstream ss(line);
    
    ss >> name >> age;

    if (age > maxAge) {
        maxAge = age;
        oldestName = name;
    }
}

file.close();

cout << "The oldest person is " << oldestName <<"."<< endl;



  //add code above this line
  
  return 0;
  
}
