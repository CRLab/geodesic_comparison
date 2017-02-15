#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <eigen3/Eigen/Eigen>

#include <iostream>
#include <vector>

using namespace std;
using namespace Eigen;

class node{
private:
    double distance;
    node* previous;
    bool has_previous;
public:
    int mat_index; //contains index in adjacency matrix
    int queue_index; //contains index in min_queue
    bool in_queue; //indicates if node is still in queue

    node(int Mindex);

    void reset();

    double setDist(double dist);
    node* setPrevious(node* prev);
    double getDist();
    bool hasPrev();
};
typedef node* nodePtr;



class min_queue{
private:
    nodePtr *heap;
    int max_size;
    int size;

    void grow();

    int percolateUp(int hole, nodePtr n);
    int percolateDown(int hole, nodePtr n);

public:
    min_queue();
    ~min_queue();

    void clear();

    void load(vector<node> &nodes);

    bool isEmpty();

    void push(nodePtr in);

    nodePtr pop();

    void decrease_priority(nodePtr n, double new_dist);

    void set_previous(nodePtr target, nodePtr prev);
};


class dijkstra{
private:
    MatrixXd* adjacency_mat;
    vector<node> nodes;
    min_queue queue;

public:
    dijkstra(MatrixXd* adjacencyMat);

    void reinitialize();

    //get all neighbors that are in the queue
    vector<int> neighbor_inds(int index);

    double compute_dist(int source_ind, int dest_ind);

    MatrixXd compute_all();
};

#endif
