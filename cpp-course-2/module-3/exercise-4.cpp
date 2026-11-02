#include <iostream>
using namespace std;

int main(int argc, char** argv) {
  
  string my_string = (argv[1]);
  
  //add code below this line

int mid = my_string.length() / 2;

cout << my_string.substr(0, mid) << endl;
cout << my_string.substr(mid) << endl;



  //add code above this line
  
  return 0;
  
}