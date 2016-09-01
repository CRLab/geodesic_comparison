#ifndef GEODESIC_H
#define GEODESIC_H

#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/kdtree/kdtree_flann.h>
#include <eigen3/Eigen/Eigen>

#include <iostream>
#include <fstream>
#include <ctime>

#include "dijkstra.h"

#define NUM_SAMPLES 200

using namespace std;
using namespace pcl;
using namespace Eigen;

class mesh{
private:
    vector<Vector3f> vertices;
    vector<Vector3i> triangles;
    vector<Vector3f> centroids;
    vector<double> triangle_areas;
    double total_area;
    vector<double> geodesic_function;

    vector<int> getSamples(int num_samples=NUM_SAMPLES) const;
    PointCloud<PointXYZ>::Ptr getCentroidCloud(const vector<int> &samples) const;

    vector<double> mat_mult(const MatrixXd &mat, const vector<double> &vec);

    //get adjacency graph with distance weights of centroid cloud
    MatrixXd getAdjacencyGraph(const vector<int> &samples, int k_neighbors);

    //implement dijkstra's algorithm to get geodesic approximation matrix
    void getGeodesicFunction(int num_samples, int k_neighbors);

public:
    //be sure to initialize srand in constructor
    mesh(const char* filename, int num_samples=NUM_SAMPLES, int k_neighbors=5); //load mesh from ply file
    void printGeodesicFunction(const char* filename);
};

#endif
