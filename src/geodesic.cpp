
#include "geodesic.h"

vector<int> mesh::getSamples(int num_samples) const{
    vector<int> indices;
    int inds[centroids.size()];
    for(int i=0; i<centroids.size(); i++){
        inds[i]=i;
    }
    // shuffle inds
    for(int i=centroids.size()-1; i>0; i--){
        int n=rand()%(i+1);
        int temp = inds[i];
        inds[i] = inds[n];
        inds[n] = temp;
    }

    for(int i=0; i<num_samples; i++){
        indices.push_back(inds[i]);
    }
    return indices;
}

PointCloud<PointXYZ>::Ptr mesh::getCentroidCloud(const vector<int> &samples) const{
    PointCloud<PointXYZ>::Ptr cloud(new PointCloud<PointXYZ>());
    for(int i=0; i<samples.size(); i++){
        int index = samples[i];
        PointXYZ pnt(centroids[index][0], centroids[index][1], centroids[index][2]);
        cloud->push_back(pnt);
    }
    return cloud;
}

//get adjacency graph with distance weights of centroid cloud
MatrixXd mesh::getAdjacencyGraph(const vector<int> &samples, int k_neighbors){
    PointCloud<PointXYZ>::Ptr cloud = getCentroidCloud(samples);
    MatrixXd graph(samples.size(),samples.size());
    //set all graph values to 1000000 to approximate inf
    for(int i=0; i<samples.size(); i++){
        for(int j=0; j<samples.size(); j++){
            graph(i,j)=1000000;
        }
    }

    //get k-nearest neighbors to fill in adjacency graph
    KdTreeFLANN<PointXYZ> kdtree;
    kdtree.setInputCloud (cloud);
    for(int i=0; i<cloud->points.size(); i++){
        PointXYZ searchPoint=cloud->points[i];
        std::vector<int> pointIdxNKNSearch(k_neighbors+1);
        std::vector<float> pointNKNSquaredDistance(k_neighbors+1);
        int num_neighbors = kdtree.nearestKSearch(searchPoint, k_neighbors+1, pointIdxNKNSearch, pointNKNSquaredDistance);
        if (num_neighbors>1){
            for(int j=0; j<num_neighbors; j++){
                float val = sqrt(pointNKNSquaredDistance[j]);
                graph(pointIdxNKNSearch[j],i) = val;
                graph(i,pointIdxNKNSearch[j]) = val;
            }
        }
        else{
            cerr<<"Nearest Neighbor search failed"<<endl;
            exit(1);
        }
    }

    return graph;
}

//multiply matrix*vector
vector<double> mesh::mat_mult(const MatrixXd &mat, const vector<double> &vec){
    assert(mat.cols()==vec.size());
    vector<double> out;
    for(int i=0; i<mat.rows(); i++){
        double val=0.0;
        int count = 0;
        for(int j=0; j<mat.cols(); j++){
            double mat_val = mat(i,j);
            if(mat_val>10000.0){
                cout<<"Disconnect: "<<i<<", "<<j<<endl;
                continue;
            }
            count++;
            val+=(mat_val*vec[j]);
        }
        out.push_back(val*vec.size()/((float)count));
    }
    return out;
}

//implement dijkstra's algorithm to get geodesic vector
void mesh::getGeodesicFunction(int num_samples, int k_neighbors){
    vector<int> samples = getSamples(num_samples);
    cout<<samples.size()<<" samples selected"<<endl;
    MatrixXd adjacency_mat = getAdjacencyGraph(samples, k_neighbors);
    cout<<"Adjacency Matrix formed"<<endl;
    dijkstra mat_comp(&adjacency_mat);
    MatrixXd geodesic_mat = mat_comp.compute_all();
    cout<<"Geodesic Matrix computed"<<endl;
    vector<double> areas;
    double sum_area=0.0;
    for(int i=0; i<samples.size(); i++){
        int index = samples[i];
        double val = triangle_areas[index];
        areas.push_back(val);
        sum_area+=val;
    }
    for(int i=0; i<samples.size(); i++){
        areas[i]/=sum_area;
    }
    geodesic_function = mat_mult(geodesic_mat, areas);
    //scale to cm
    // for(int i=0; i<geodesic_function.size(); i++){
    //     geodesic_function[i]*=100.0;
    // }
}

//print to file as .hist
//first line=#entries
//second line=space deliminated entries
void mesh::printGeodesicFunction(const char* filename){
    ofstream myfile;
    myfile.open (filename);
    myfile << geodesic_function.size()<<endl;
    for(int i=0; i<geodesic_function.size(); i++){
        myfile << geodesic_function[i]<<" ";
    }
    myfile.close();
}


mesh::mesh(const char *filename, int num_samples, int k_neighbors){
    int num_vertices=-1;
    int num_faces=-1;

    ifstream myfile(filename);
    if(myfile.is_open()){
        string line;
        //parse header
        while (getline(myfile, line)){
            if(strcmp(line.substr(0,10).c_str(), "end_header")==0) break;
            else if(strcmp(line.substr(0,12).c_str(), "element face")==0){
                string nfaces = line.substr(13, string::npos);
                num_faces = atoi(nfaces.c_str());
            }
            else if(strcmp(line.substr(0,14).c_str(), "element vertex")==0){
                string nverts = line.substr(15, string::npos);
                num_vertices = atoi(nverts.c_str());
            }
        }
        if(num_vertices<0 || num_faces<0){
            cerr<<"Ply file not formatted properly"<<endl;
            exit(1);
        }
        //retrieve vertices
        for(int i=0; i<num_vertices; i++){
            if(!getline(myfile, line)){
                cerr<<"Vertices not found in Ply file"<<endl;
                exit(1);
            }
            Vector3f v;
            char line_cstr[line.length()];
            strcpy(line_cstr, line.c_str());
            v[0] = 100*atof(strtok(line_cstr, " "));
            v[1] = 100*atof(strtok(NULL, " "));
            v[2] = 100*atof(strtok(NULL, " "));
            vertices.push_back(v);
        }
        //retrieve triangles
        for(int i=0; i<num_faces; i++){
            if(!getline(myfile, line)){
                cerr<<"Faces not found in Ply file"<<endl;
                exit(1);
            }
            Vector3i t;
            char line_cstr[line.length()];
            strcpy(line_cstr, line.c_str());
            strtok(line_cstr, " ");
            t[0] = atoi(strtok(NULL, " "));
            t[1] = atoi(strtok(NULL, " "));
            t[2] = atoi(strtok(NULL, " "));
            triangles.push_back(t);
        }
        myfile.close();
    }
    else{
        cerr<<"Failed to open file"<<endl;
        exit(1);
    }

    cout<<"Ply file loaded"<<endl;

    //compute centroids and areas of triangles
    for(int i=0; i<triangles.size(); i++){
        Vector3f p1 = vertices[triangles[i][0]];
        Vector3f p2 = vertices[triangles[i][1]];
        Vector3f p3 = vertices[triangles[i][2]];
        Vector3f centroid = p1+p2+p3;
        centroid[0]/=3.0; centroid[1]/=3.0; centroid[2]/=3.0;
        double len1 = sqrt((p2[0]-p1[0])*(p2[0]-p1[0])+(p2[1]-p1[1])*(p2[1]-p1[1])+(p2[2]-p1[2])*(p2[2]-p1[2]));
        double len2 = sqrt((p3[0]-p2[0])*(p3[0]-p2[0])+(p3[1]-p2[1])*(p3[1]-p2[1])+(p3[2]-p2[2])*(p3[2]-p2[2]));
        double len3 = sqrt((p1[0]-p3[0])*(p1[0]-p3[0])+(p1[1]-p3[1])*(p1[1]-p3[1])+(p1[2]-p3[2])*(p1[2]-p3[2]));
        double s = (len1+len2+len3)/2.0;
        double area_squared = s*(s-len1)*(s-len2)*(s-len3);
        double area;
        if(area_squared<=0.000000001) area=0.000000001;
        else area = sqrt(area_squared);
        centroids.push_back(centroid);
        triangle_areas.push_back(area);
        total_area+=area;
    }

    cout<<"Centroids and areas computed"<<endl;
    cout<<"Total Area: "<<total_area<<" cm^2"<<endl;

    //seed the random number generator
    srand(time(NULL));

    if(num_samples>triangles.size()) num_samples = triangles.size();
    //get geodesic vector
    getGeodesicFunction(num_samples, k_neighbors);
}
