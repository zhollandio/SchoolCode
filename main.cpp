#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include "graph.h"
#include "stack.h"
#include "queue.h"
#include "priorityqueue.h"
using namespace std;

Graph loadMaze(string filename, int &start, int &end)
{
	ifstream fin;
	fin.open(filename.c_str());
	
	int V;
	string s;
	
	fin >> V >> start >> end;
	
	if(!fin)
	{
		cerr << "Failed to load " << filename << "!" << endl;
		exit(1);
	}
	
	Graph g(V);
	for(int i = 0; i < V; i++)
	{
		for(int j = 0; j < V; j++)
		{
			fin >> s;
			if(s != "inf")
				g.addEdge(i, j, atoi(s.c_str()));
		}
	}
	
	fin.close();
	
	return g;
}

void shortestPath1(Graph& g, int start, int end);
void shortestPath2(Graph& g, int start, int end);
void shortestPath3(Graph& g, int start, int end);

int main()
{
	Graph g;
	int start, end;
	
	// Floor 1: one guard per room; find the path with the fewest guards
	g = loadMaze("floor-1.txt", start, end);
	// todo: fill in your algorithm here; output # guards fought, # steps taken, and the path selected
	cout << "Floor 1:" << endl;
	shortestPath1(g,start, end);
	
	// Floor 2: no guards; find any path quickly, assuming the end is far away from the start
	g = loadMaze("floor-2.txt", start, end);
	// todo: fill in your algorithm here; output # guards fought, # steps taken, and the path selected
	cout << endl << "Floor 2:" << endl;
	shortestPath2(g, start, end);

	// Floor 3: many guards per room; find the path with the fewest guards
	g = loadMaze("floor-3.txt", start, end);
	// todo: fill in your algorithm here; output # guards fought, # steps taken, and the path selected
	cout << endl << "Floor 3:" << endl;
	shortestPath3(g, start, end);

	return 0;
}


// 1 guard in every room
// use BFS to find shortest path
void shortestPath1(Graph& g, int start, int end)
{
	// declare
	int* cost = new int[g.numVertices()];
	int* path = new int[g.numVertices()];
	bool* visited = new bool[g.numVertices()];
	int steps = 0;
	int numGuardsFought = 0;

	// initialize
	for (int i = 0; i < g.numVertices(); i++)
	{
		cost[i] = 0;
		path[i] = -1;
		visited[i] = false; 
	}

	Queue<int> q; // store search nodes

	// push start node
	q.push(start);

	// initialize to start
	path[start] = start;
	cost[start] = 0;
	visited[start] = true;

	// loop till queue empty
	while (q.size() > 0)
	{

		int current = q.front(); // get current node
		q.pop();

		steps++; // count steps

		// end found?
		if (current == end) break;

		// for each neighbor of current
		for (int next = 0; next < g.numVertices(); next++)
		{
			// has edge?
			if (g.hasEdge(current, next))
			{
				// calculate new cost
				int newCost = cost[current] + g.getWeight(current, next);

				  // if not visited or lower cost
				  // only store nodes not visited or lower cost
				  if (!visited[next] || newCost < cost[next]) {
					  
					  // count guards fought
					  numGuardsFought += g.getWeight(current, next);
					  
					  cost[next] = newCost; // store new cost
					  q.push(next); // store next node
					  path[next] = current; // store path
					  visited[next] = true; // store visited
				  }
			}
		}
	}

	// print output
	cout << "Steps: " << steps << endl;
	cout << "Num guards fought: " << numGuardsFought << endl;
	
	// print path
	cout << "Path:" << endl;

	    // stack to print path
		Stack<int> s;
		
		// get path from end to start
		int current = end;
		s.push(current);
		while (current != start) {
			current = path[current];
			s.push(current);
		}
	
		// print path
		while (s.size() > 0)
		{
			cout << s.top() << " ";
			s.pop();
		}

		cout << endl;

		// free memory
		delete[] cost;
		delete[] path;
		delete[] visited;
	}

// no guard in a room 
// store nodes of closest distance to end
void shortestPath2(Graph& g, int start, int end)
{
	// declare
	int* cost = new int[g.numVertices()];
	int* path = new int[g.numVertices()];
	bool* visited = new bool[g.numVertices()];
	int steps = 0;
	int numGuardsFought = 0;

	// initialize
	for (int i = 0; i < g.numVertices(); i++)
	{
		cost[i] = 0;
		path[i] = -1;
		visited[i] = false;
	}

	Queue<int> q;  // queue to store cloests nodes to end

	// push start node
	q.push(start);


	// initialize
	path[start] = start;
	cost[start] = 0;
	visited[start] = true;

	// loop till queue empty
	while (q.size() > 0)
	{
		// get curent node
		int current = q.front();
		q.pop();

		steps++; // count steps

		// end found?
		if (current == end) break;

		// for each neighbor of current
		for (int next = 0; next < g.numVertices(); next++)
		{
			// has edge?
			if (g.hasEdge(current, next))
			{
				// new cost is closest to end
				int newCost = cost[current] + (end-next);

				// node not visited or closer to end
				if (!visited[next] || newCost < cost[next]) {
					
					// finf guards if any?
					numGuardsFought += g.getWeight(current, next);
					
					cost[next] = newCost; // store new cost
					q.push(next); // store minimum node
					path[next] = current; // store path
					visited[next] = true; // mark visited
				}
			}
		}
	}

	// print output
	cout << "Steps: " << steps << endl;
	cout << "Num guards fought: " << numGuardsFought << endl;
	cout << "Path:" << endl;
	
	// stack to print path
	Stack<int> s;

	// get path from end to start
	int current = end;
	s.push(current);
	while (current != start) {
		current = path[current];
		s.push(current);
	}

	// print path
	while (s.size() > 0)
	{
		cout << s.top() << " ";
		s.pop();
	}

	cout << endl;

	// free memory
	delete[] cost;
	delete[] path;
	delete[] visited;
}

// many guards in a room
// use A* algorithm to minimize steps
// add cloest distance to cost
void shortestPath3(Graph& g, int start, int end)
{
	// declare
	int* cost = new int[g.numVertices()];
	int* path = new int[g.numVertices()];
	bool* visited = new bool[g.numVertices()];
	int steps = 0;
	int numGuardsFought = 0;

	// intialize 
	for (int i = 0; i < g.numVertices(); i++)
	{
		cost[i] = 0;
		path[i] = -1;
		visited[i] = false;
	}

    // use priority queue to store next minimum node 
	// priority is distance to end node
	PriorityQueue<int> q; 

	// push start node
	q.push(start, 0);

	// initialize to start
	path[start] = start;
	cost[start] = 0;
	visited[start] = true;

	// loop till queue empty
	while (q.size() > 0)
	{
		// get current node
		int current = q.front();
		q.pop();
		steps++;

		// end ?
		if (current == end) break;

		// for each neighbor of current
		for (int next = 0; next < g.numVertices(); next++)
		{
			// has edge?
			if (g.hasEdge(current, next))
			{
				// calculate new cost
				int newCost = cost[current] + g.getWeight(current, next);

				// if not visited or lower cost found 
				if (!visited[next] || newCost < cost[next]) {
					
					// count fought guards
					numGuardsFought += g.getWeight(current, next);
				
					
					cost[next] = newCost; // store new cost
					int priority = newCost + (next - end); // calculate priority
					q.push(next, priority); // store node and priority
					path[next] = current; // store path
					visited[next] = true; // mark visited
				}
			}
		}
	}


	// print output
	cout << "Steps: " << steps << endl;
	cout << "Num guards fought: " << numGuardsFought << endl;
	cout << "Path:" << endl;

	// stack to print path
	Stack<int> s;

	// get path end to start
	int current = end;
	s.push(current);
	while (current != start) {
		current = path[current];
		s.push(current);
	}

	// print path
	while (s.size() > 0)
	{
		cout << s.top() << " ";
		s.pop();
	}

	cout << endl;

	// free memory
	delete[] cost;
	delete[] path;
	delete[] visited;
}

