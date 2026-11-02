#include <iostream>
using namespace std;

//add class definitions below this line
class Watch {
  private:
    string manufacturer;
    string model;
    int diameter;
    int water_resistance;
    string material;

  public:
    Watch(string m, string mo, int d, int w, string ma) {
      manufacturer = m;
      model = mo;
      diameter = d;
      water_resistance = w;
      material = ma;
    }

    string GetManufacturer() {
      return manufacturer;
    }

    void SetManufacturer(string m) {
      manufacturer = m;
    }

    string GetModel() {
      return model;
    }

    void SetModel(string mo) {
      model = mo;
    }

    int GetDiameter() {
      return diameter;
    }

    void SetDiameter(int d) {
      diameter = d;
    }

    int GetWaterResistance() {
      return water_resistance;
    }

    void SetWaterResistance(int w) {
      water_resistance = w;
    }

    string GetMaterial() {
      return material;
    }

    void SetMaterial(string ma) {
      material = ma;
    }

    void Summary() {
      cout << "Manufacturer: " << manufacturer << endl;
      cout << "Model: " << model << endl;
      cout << "Diameter: " << diameter << " mm" << endl;
      cout << "Water Resistance: " << water_resistance << " m" << endl;
      cout << "Material: " << material << endl;
    }
};


//add class definitions above this line


int main() {
  
  //DO NOT EDIT CODE BELOW THIS LINE

  Watch my_watch("Omega", "Speedmaster", 42, 50, "steel");
  cout << my_watch.GetManufacturer() << endl;
  cout << my_watch.GetModel() << endl;
  cout << my_watch.GetDiameter() << endl;
  cout << my_watch.GetWaterResistance() << endl;
  cout << my_watch.GetMaterial() << endl;
  my_watch.SetManufacturer("Rolex");
  my_watch.SetModel("Explorer");
  my_watch.SetDiameter(36);
  my_watch.SetWaterResistance(60);
  my_watch.SetMaterial("gold");
  my_watch.Summary();

  //DO NOT EDIT CODE ABOVE THIS LINE
  
  return 0;
  
}