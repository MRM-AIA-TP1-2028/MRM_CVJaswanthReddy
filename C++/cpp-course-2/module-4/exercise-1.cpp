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
string read;
int lines = 0;
int characters = 0;

while (getline(file, read)) {
    lines++;
    characters += read.length();
}

file.close();

cout << lines << " line(s)" << endl;
cout << characters << " character(s)" << endl;

  
  //add code above this line
  
  return 0;
  
}