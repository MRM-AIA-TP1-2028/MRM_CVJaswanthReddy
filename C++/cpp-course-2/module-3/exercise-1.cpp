#include <iostream>
using namespace std;

int main(int argc, char** argv) {
  
  string my_string = (argv[1]);
  
  //add code below this line

cout << my_string.at(0) << " is the first character and "
     << my_string.at(my_string.length() - 1)
     << " is the last character" << endl;



  //add code above this line
  
  return 0;
  
}