
#include "geodesic.h"

#include <iostream>

using namespace std;

int main(int argc, char **argv){
    if(argc!=3){
        cout<<"Usage: <Input filename (.ply)> <Output filename (.hist)>"<<endl;
        return 1;
    }

    const char* infname = argv[1];
    const char* outfname = argv[2];

    mesh m(infname);
    m.printGeodesicFunction(outfname);
}
