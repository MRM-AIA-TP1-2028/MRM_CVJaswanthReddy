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
string city;
string country;
string latitude;
string longitude;
bool first = true;

getline(file, line);

cout << "The following cities are in the Southern Hemisphere: ";

while (getline(file, line)) {
    stringstream ss(line);

    getline(ss, city, ',');
    getline(ss, country, ',');
    getline(ss, latitude, ',');
    getline(ss, longitude, ',');

    if (stoi(latitude) < 0) {
        if (!first) {
            cout << ", ";
        }

        cout << city;
        first = false;
    }
}

cout << "." << endl;

file.close();



  //add code above this line
  
  return 0;
  
}
