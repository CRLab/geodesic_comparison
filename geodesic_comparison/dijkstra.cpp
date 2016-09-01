
#include "dijkstra.h"

node::node(int Mindex){
    distance = 100000; //set to inf
    previous = 0;
    has_previous = false;

    mat_index=Mindex;
    queue_index=0;
    in_queue=true;
}

void node::reset(){
    distance = 100000;
    previous = 0;
    has_previous = false;

    queue_index=0;
    in_queue=true;
}


double node::setDist(double dist){
    distance=dist;
}

node* node::setPrevious(node* prev){
    previous=prev;
    has_previous=true;
}

double node::getDist(){
    return distance;
}

bool node::hasPrev(){
    return has_previous;
}




void min_queue::grow(){
    nodePtr *new_heap = new nodePtr[max_size*2];
    for(int i=0; i<max_size; i++){
        new_heap[i]=heap[i];
    }
    delete [] heap;
    heap=new_heap;
    max_size*=2;
}

int min_queue::percolateUp(int hole, nodePtr n) {
    while (hole > 1 && (n->getDist()<heap[hole/2]->getDist())){
        heap[hole] = heap[hole/2];
        heap[hole]->queue_index=hole;
        hole /= 2;
    }
    return hole;
}

int min_queue::percolateDown(int hole, nodePtr n){
    while (2*hole <= size) {
        int left = 2*hole;
        int right = left + 1;
        int target;

        if (right<=size && heap[right]->getDist()<heap[left]->getDist()) target = right;
        else target = left;

        if (heap[target]->getDist()<n->getDist()) {
            heap[hole] = heap[target];
            heap[hole]->queue_index=hole;
            hole = target;
        }
        else break;
    }
    return hole;
}

min_queue::min_queue(){
    max_size=0;
    size=0;
    heap=0;
}

min_queue::~min_queue(){
    if(size>0) clear();
}

void min_queue::clear(){
    delete [] heap;
    size=0;
}

void min_queue::load(vector<node> &nodes){
    max_size=nodes.size();
    size=0;
    heap = new nodePtr[max_size+1];
    for(int i=0; i<nodes.size(); i++){
        push(&(nodes[i]));
    }
}

bool min_queue::isEmpty(){
    return size==0;
}

void min_queue::push(nodePtr in){
    size++;
    if(size==max_size+1) grow();
    int newPos = percolateUp(size, in);
    heap[newPos] = in;
    heap[newPos]->queue_index=newPos;
}

nodePtr min_queue::pop(){
    assert(!isEmpty());
    nodePtr returnVal = heap[1];
    heap[1]->in_queue=false;
    size--;
    int newPos = percolateDown(1, heap[size+1]);
    heap[newPos] = heap[size+1];
    heap[newPos]->queue_index=newPos;
    return returnVal;
}

void min_queue::decrease_priority(nodePtr n, double new_dist){
    assert(new_dist<=n->getDist());
    int hole = n->queue_index;
    n->setDist(new_dist);
    int newPos = percolateUp(hole, n);
    heap[newPos] = n;
    n->queue_index=newPos;
}

void min_queue::set_previous(nodePtr target, nodePtr prev){
    target->setPrevious(prev);
}

dijkstra::dijkstra(MatrixXd* adjacencyMat){
    adjacency_mat = adjacencyMat;
    for(int i=0; i<adjacency_mat->rows(); i++){
        node n(i);
        nodes.push_back(n);
    }
}

void dijkstra::reinitialize(){
    queue.clear();
    for(int i=0; i<nodes.size(); i++){
        nodes[i].reset();
    }
}

//get all neighbors that are in the queue
vector<int> dijkstra::neighbor_inds(int index){
    vector<int> neighbors;
    for(int i=0; i<nodes.size(); i++){
        if(i==index) continue;
        if((*adjacency_mat)(index, i)<999999){
            if(nodes[i].in_queue){
                neighbors.push_back(i);
            }
        }
    }
    return neighbors;
}

double dijkstra::compute_dist(int source_ind, int dest_ind){
    //set source dist to 0
    nodes[source_ind].setDist(0.0);
    //load queue
    queue.load(nodes);
    while(!queue.isEmpty()){
        nodePtr n_ptr = queue.pop();
        //check if reached destination
        if(n_ptr->mat_index==dest_ind) break;
        //get neighors in queue
        vector<int> neighbors = neighbor_inds(n_ptr->mat_index);
        for(int i=0; i<neighbors.size(); i++){
            double alt = n_ptr->getDist() + (*adjacency_mat)(n_ptr->mat_index, neighbors[i]);
            if(alt<nodes[neighbors[i]].getDist()){
                queue.set_previous(&(nodes[neighbors[i]]), n_ptr);
                queue.decrease_priority(&(nodes[neighbors[i]]), alt);
            }
        }
    }

    double return_val = nodes[dest_ind].getDist();
    reinitialize();
    return return_val;
}

MatrixXd dijkstra::compute_all(){
    MatrixXd dist_mat(adjacency_mat->rows(), adjacency_mat->cols());
    for(int i=0; i<adjacency_mat->rows(); i++){
        for(int j=i; j<adjacency_mat->cols(); j++){
            double dist=compute_dist(i,j);
            dist_mat(j,i) = dist*dist;
            dist_mat(i,j)=dist_mat(j,i);
        }
    }
    return dist_mat;
}
