#include <iostream>
using namespace std;

int main(int argc, char** argv) {
  
  string my_string = (argv[1]);
  
  //add code below this line

for (int i = 0; i < my_string.length(); i += 2) {
    char temp = my_string.at(i);
    my_string.at(i) = my_string.at(i + 1);
    my_string.at(i + 1) = temp;
}

cout << my_string << endl;



  //add code above this line
  
  return 0;
  
}