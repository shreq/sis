#include <iostream>
#include "Fifteen.hpp"

using namespace std;

int main()
{
    cout << "- - S T A R T - -\n\n";

	shared_ptr<Fifteen> f = make_shared<Fifteen>("manh", "./../start.txt");

	f->astar();

	cout << "\n\n- - -S T O P- - -\n";
}
