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
vector<string> lines;
string read;

while (getline(file, read)) {
    lines.push_back(read);
}

file.close();

for (int i = lines.size() - 1; i >= 0; i--) {
    cout << lines[i] << endl;
}



  //add code above this line
  
  return 0;
  
}
