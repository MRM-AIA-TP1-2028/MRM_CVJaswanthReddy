#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;

//add class definitions below this line

class Median {
  public:
    double CalculateMedian(int a, int b) {
      vector<int> nums = {a, b};
      sort(nums.begin(), nums.end());
      return (double)(nums[0] + nums[1]) / 2;
    }

    double CalculateMedian(int a, int b, int c) {
      vector<int> nums = {a, b, c};
      sort(nums.begin(), nums.end());
      return nums[1];
    }

    double CalculateMedian(int a, int b, int c, int d) {
      vector<int> nums = {a, b, c, d};
      sort(nums.begin(), nums.end());
      return (double)(nums[1] + nums[2]) / 2;
    }

    double CalculateMedian(int a, int b, int c, int d, int e) {
      vector<int> nums = {a, b, c, d, e};
      sort(nums.begin(), nums.end());
      return nums[2];
    }
};

//add class definitions above this line

int main() {
  Median m;
  cout << m.CalculateMedian(3, 5, 1, 4, 2) << endl;
  cout << m.CalculateMedian(8, 6, 4, 2) << endl;
  cout << m.CalculateMedian(9, 3, 7) << endl;
  cout << m.CalculateMedian(5, 2) << endl;

  Median m2;
  cout << m2.CalculateMedian(24, 22, 21, 23, 20) << endl;
  cout << m2.CalculateMedian(12, 18, 9, 3) << endl;
  cout << m2.CalculateMedian(0, 1, 0) << endl;
  cout << m2.CalculateMedian(5, 3) << endl;

  return 0;
}