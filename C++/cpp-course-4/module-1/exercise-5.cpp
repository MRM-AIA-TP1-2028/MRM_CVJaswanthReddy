#include <iostream>
using namespace std;

//add class definitions below this line
class CardBinder {
  private:
    int gold_card;
    int silver_card;

  public:
    CardBinder() {
      gold_card = 0;
      silver_card = 0;
    }

    int GetGold() {
      return gold_card;
    }

    int GetSilver() {
      return silver_card;
    }

    int GetTotal() {
      return gold_card + silver_card;
    }

    void AddGold(int n) {
      if (n <= 0) {
        cout << "You cannot add a negative or 0 amount of cards." << endl;
      }
      else if (gold_card + silver_card + n > 20) {
        cout << "You do not have enough binder room." << endl;
      }
      else {
        gold_card += n;
      }
    }

    void AddSilver(int n) {
      if (n <= 0) {
        cout << "You cannot add a negative or 0 amount of cards." << endl;
      }
      else if (gold_card + silver_card + n > 20) {
        cout << "You do not have enough binder room." << endl;
      }
      else {
        silver_card += n;
      }
    }

    void RemoveGold(int n) {
      if (n <= 0) {
        cout << "You cannot remove a negative or 0 amount of cards." << endl;
      }
      else if (gold_card - n < 0) {
        cout << "You do not have enough gold cards to remove." << endl;
      }
      else {
        gold_card -= n;
      }
    }

    void RemoveSilver(int n) {
      if (n <= 0) {
        cout << "You cannot remove a negative or 0 amount of cards." << endl;
      }
      else if (silver_card - n < 0) {
        cout << "You do not have enough silver cards to remove." << endl;
      }
      else {
        silver_card -= n;
      }
    }
};


//add class definitions above this line


int main() {
  
  //DO NOT EDIT CODE BELOW THIS LINE

  CardBinder cb;
  cb.AddGold(21);
  cb.AddGold(11);
  cb.AddSilver(-4);
  cb.AddSilver(8);
  cb.RemoveGold(12);
  cb.RemoveGold(4);
  cb.RemoveSilver(-2);
  cb.RemoveSilver(6);
  cout << cb.GetGold() << endl;
  cout << cb.GetSilver() << endl;
  cout << cb.GetTotal() << endl;
  

  //DO NOT EDIT CODE ABOVE THIS LINE
  
  return 0;
  
}