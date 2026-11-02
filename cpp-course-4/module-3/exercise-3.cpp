#include <iostream>
#include <vector>
using namespace std;

//DO NOT EDIT/////////////////////////////////////
class Temperature {
  public:
    virtual double Celsius(double temp) = 0;
    virtual double Fahrenheit(double temp) = 0;
};
//////////////////////////////////////////////////

//add class definitions below this line

class Conversion : public Temperature {
  public:
    double Celsius(double temp) {
      return (temp - 32) * 5 / 9;
    }

    double Fahrenheit(double temp) {
      return (temp * 9 / 5) + 32;
    }

    double ConvertTo(char unit, double temp) {
      if (unit == 'c' || unit == 'C') {
        return Celsius(temp);
      }
      else if (unit == 'f' || unit == 'F') {
        return Fahrenheit(temp);
      }
      else {
        return -0.0001;
      }
    }
};

//add class definitions above this line

int main() {

  Conversion c;
  cout << c.ConvertTo('c', 212.0) << endl;
  cout << c.ConvertTo('C', 78.0) << endl;
  cout << c.ConvertTo('h', 23.0) << endl;
  cout << c.ConvertTo('F', 0.0) << endl;
  cout << c.ConvertTo('f', 29.0) << endl;
  cout << c.ConvertTo('3', 112.0) << endl;

  return 0;
}