#pragma once

#include <string>
#include <vector>
#include <memory>

class Fifteen
{
public:
	std::string heur = "";
	std::vector<std::vector<int>> tiles;
	std::string undo_move = "";
	double h_score = 0;
	int depth = 0;
	double f_score = 0;
	std::vector<std::string> previous_moves;

	Fifteen(std::string, std::string);
	Fifteen(std::shared_ptr<Fifteen>);
	virtual ~Fifteen();

	std::string tiles2str();
	std::vector<int> find(int = 0);
	void swap(std::string, int = -1, int = -1);
	double heuristic();
	std::vector<std::shared_ptr<Fifteen>> generate_next_states();

	void astar();
};
