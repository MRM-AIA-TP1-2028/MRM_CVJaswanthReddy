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
int sums[4] = {0, 0, 0, 0};

while (getline(file, line)) {
    stringstream ss(line);
    string value;

    for (int i = 0; i < 4; i++) {
        getline(ss, value, ',');
        sums[i] += stoi(value);
    }
}

file.close();

for (int i = 0; i < 4; i++) {
    cout << sums[i] / 3;

    if (i < 3) {
        cout << " ";
    }
}

cout << endl;



  //add code above this line
  
  return 0;
  
}
