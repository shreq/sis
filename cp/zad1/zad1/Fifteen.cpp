#include "Fifteen.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <deque>
#include <algorithm>

using namespace std;

template <class T, class K>
bool is_contained(T container, K obj)
{
	for (auto element : container)
		if (element->tiles == obj->tiles)
			return true;
	return false;
}

template <class T>
void swap_(T a, T b)
{
	T x = a;
	a = b;
	b = x;
}

Fifteen::Fifteen(string heur, string filepath)
{
	ifstream fin;
	fin.open(filepath.c_str());

	this->heur = heur;

	for (int y = 0; y < 4; y++)
	{
		vector<int> v(0);

		for (int x = 0, t; x < 4; x++, fin >> t, v.push_back(t));

		this->tiles.push_back(v);
	}

	fin.close();
}

Fifteen::Fifteen(shared_ptr<Fifteen> parent)
{
	this->heur = parent->heur;
	this->tiles = parent->tiles;
	this->undo_move = parent->undo_move;
	this->depth = parent->depth;
	this->previous_moves = parent->previous_moves;
}

Fifteen::~Fifteen() {}

string Fifteen::tiles2str()
{
	stringstream s;

	for (size_t y = 0; y < this->tiles.size(); y++, s << '\n')
		for (size_t x = 0; x < this->tiles[y].size(); x++)
			s << this->tiles[y][x] << ' ';

	return s.str();
}

vector<int> Fifteen::find(int tile)
{
	vector<int> v(0);
	for (size_t y = 0; y < this->tiles.size(); y++)
		for (size_t x = 0; x < this->tiles[y].size(); x++)
			if (this->tiles[y][x] == tile)
			{
				v.push_back(x);
				v.push_back(y);
				return v;
			}

	throw exception();
}

void Fifteen::swap(string d, int x, int y)
{
	if (x == -1 or y == -1)
	{
		vector<int> v = this->find();
		x = v[0];
		y = v[1];
	}

	if (d == "u" and y - 1 >= 0)
	{
		swap_(this->tiles[y][x], this->tiles[y - 1][x]);
		this->previous_moves.push_back("u");
		this->undo_move = "d";
	}
	else if (d == "d" and y + 1 <= int(this->tiles.size()) - 1)
	{
		swap_(this->tiles[y][x], this->tiles[y + 1][x]);
		this->previous_moves.push_back("d");
		this->undo_move = "u";
	}
	else if (d == "l" and x - 1 >= 0)
	{
		swap_(this->tiles[y][x], this->tiles[y][x - 1]);
		this->previous_moves.push_back("l");
		this->undo_move = "r";
	}
	else if (d == "r" and x + 1 <= int(this->tiles[y].size()) - 1)
	{
		swap_(this->tiles[y][x], this->tiles[y][x + 1]);
		this->previous_moves.push_back("r");
		this->undo_move = "l";
	}
	else
		throw exception();
}

double Fifteen::heuristic()
{
	if (this->heur == "hamm")
	{
		int diff = 0;
		for (size_t y = 0; y < this->tiles.size(); y++)
		{
			for (size_t x = 0; x < this->tiles[y].size(); x++)
			{
				if (y == this->tiles.size() - 1 and x == this->tiles[y].size() - 1)
					if (this->tiles[y][x] != 0)
						diff++;

				else if (this->tiles[y][x] != y * this->tiles.size() + x + 1)
					diff++;
			}
		}

		return diff;
	}
	else
	{
		double score = 0;
		double value = 1;

		for (size_t y = 0; y < this->tiles.size(); y++)
		{
			for (size_t x = 0; x < this->tiles[y].size(); x++)
			{
				if (value == 16)
					value = 0;

				vector<int> v = this->find();
				int x_real = v[0], y_real = v[1];
				double dx = abs(int(x) - x_real);
				double dy = abs(int(y) - y_real);
				score += dx + dy;
				value += 1;
			}
		}

		return score;
	}
}

vector<shared_ptr<Fifteen>> Fifteen::generate_next_states()
{
	vector<int> pos = this->find();
	int x = pos[0];
	int y = pos[1];

	vector<shared_ptr<Fifteen>> next_states(0);

	if (y - 1 >= 0 and this->undo_move != "u")
	{
		auto child = make_shared<Fifteen>(*this);
		child->swap("u");
		child->depth = child->previous_moves.size() + 1;
		next_states.emplace_back(child);
	}
	if (y + 1 <= int(this->tiles.size()) - 1 and this->undo_move != "d")
	{
		auto child = make_shared<Fifteen>(*this);
		child->swap("d");
		child->depth = child->previous_moves.size() + 1;
		next_states.emplace_back(child);
	}
	if (x - 1 >= 0 and this->undo_move != "l")
	{
		auto child = make_shared<Fifteen>(*this);
		child->swap("l");
		child->depth = child->previous_moves.size() + 1;
		next_states.emplace_back(child);
	}
	if (x + 1 <= int(this->tiles[y].size()) - 1 and this->undo_move != "r")
	{
		auto child = make_shared<Fifteen>(*this);
		child->swap("r");
		child->depth = child->previous_moves.size() + 1;
		next_states.emplace_back(child);
	}

	return next_states;
}

void Fifteen::astar()
{
	deque<shared_ptr<Fifteen>> queue;
	queue.emplace_back(this);

	vector<shared_ptr<Fifteen>> processed(0);
	size_t loops = 0;

	while (queue.size() > 0 and loops < 10)
	{
		shared_ptr<Fifteen> current_state = queue[0];
		queue.pop_front();

		if (is_contained(processed, current_state))
			continue;

		/*if (loops % 2000 == 0 or current_state->heuristic() <= 5)
		{
			cout << current_state->heuristic() << ' '
				<< current_state->depth << '\t'
				<< queue.size()
				<< current_state->tiles[0][0] << '\t'
				<< current_state->previous_moves[0] << '\n';
		}*/

		if (current_state->heuristic() == 0)
		{
			cout << "\nDone!\n" << current_state->tiles2str() << '\n' << current_state->previous_moves[0] << endl;
			return;
		}

		processed.push_back(current_state);

		if (current_state->depth < 64)
		{
			for (auto state : current_state->generate_next_states())
			{
				if (is_contained(processed, state))// or is_contained(queue, state))
					continue;
				state->h_score = state->heuristic();
				state->f_score = state->h_score + state->depth;
				queue.push_back(state);
			}

			sort(queue.begin(), queue.end(), [](const shared_ptr<Fifteen> a, const shared_ptr<Fifteen> b) -> bool
			{
				return a->f_score > b->f_score;
			});
		}

		loops++;
	}
}
