#include <iostream>
#include <vector>
using namespace std;

//add code below this line

bool IsPalindrome(string word) {
    int left = 0;
    int right = word.length() - 1;

    while (left < right) {
        if (word[left] != word[right]) {
            return false;
        }

        left++;
        right--;
    }

    return true;
}



//add code above this line

int main(int argc, char** argv) {
  string x = argv[1];
  cout << boolalpha << IsPalindrome(x) << endl;
}