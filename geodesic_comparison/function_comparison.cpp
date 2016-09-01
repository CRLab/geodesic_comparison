
#include "integral.h"

using namespace std;

int main(int argc, char **argv){
    if(argc!=3){
        cout<<"Usage: <Histogram filename 1> <Histogram filename 2>"<<endl;
        return 1;
    }

    shape_distribution distribution1(argv[1]);
    shape_distribution distribution2(argv[2]);
    //shape_distribution distribution1("../../data/analysis_results/rubbermaid_ice_guard_pitcher_blue/1_1_17/partial.hist");
    //shape_distribution distribution2("../../data/analysis_results/rubbermaid_ice_guard_pitcher_blue/1_1_17/gt.hist");

    double divergence = getDivergence(distribution1, distribution2);
    cout<<divergence<<endl;
}
