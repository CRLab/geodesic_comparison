#include "integral.h"

#pragma optimize( "[optimization-list]", {on | off} ) 

//functions for getting median of list
bool sort_l2h(double i, double j){
    return (i<j);
}
double getMedian(vector<double> vec){
    sort(vec.begin(), vec.end(), sort_l2h);
    double med=vec[vec.size()/2];
    if(vec.size()%2==0){
        med+=vec[(vec.size()/2)-1];
        med/=2.0;
    }
    return med;
}
//gaussian kernel
double K(double x){
    double out = -(x*x)/2;
    out = exp(out);
    out/=sqrt(2*PI);
    return out;
}


//functional implementations

//construct shape distribution from histogram file
shape_distribution::shape_distribution(const char* filename){
    ifstream myfile(filename);
    if(!myfile.is_open()){
        cerr<<"Failed to open file"<<endl;
        exit(1);
    }
    string line;
    if(!getline(myfile, line)){
        cerr<<"File not formatted properly"<<endl;
        exit(1);
    }
    int num_entries = atoi(line.c_str());
    if(!getline(myfile, line)){
        cerr<<"File not formatted properly"<<endl;
        exit(1);
    }
    char line_cstr[line.length()];
    strcpy(line_cstr, line.c_str());
    double entrie1 = atof(strtok(line_cstr, " "));
    global_geodesic.push_back(entrie1);
    for(int i=1; i<num_entries; i++){
        const char* entrie = strtok(NULL, " ");
        if(entrie==NULL){
            cerr<<"Number of entries in histogram does not match"<<endl;
            exit(1);
        }
        global_geodesic.push_back(atof(entrie));
    }
    myfile.close();

    //compute h
    double med=getMedian(global_geodesic);
    vector<double> med_diff;
    for(int i=0; i<global_geodesic.size(); i++){
        med_diff.push_back(fabs(global_geodesic[i]-med));
    }
    double alpha=getMedian(med_diff);
    h = 243.0/(70.0*sqrt(PI)*global_geodesic.size());
    h = pow(h, 0.2);
    h = h*alpha;
}

double shape_distribution::operator()(double x) const{
    double out=0.0;
    for(int i=0; i<global_geodesic.size(); i++){
        double in=x-global_geodesic[i];
        out+=K(in/h);
    }
    out/=(h*(double)global_geodesic.size());
    return out;
}


functional_sum_div_2::functional_sum_div_2(const functional* f_1, const functional* f_2){
    f1=f_1;
    f2=f_2;
}
double functional_sum_div_2::operator()(double x) const{
    return ((*f1)(x)+(*f2)(x))/2.0;
}

log_2_functional::log_2_functional(const functional* f_){
    f=f_;
}
double log_2_functional::operator()(double x) const{
    double v = (*f)(x);
    if(v<0.00000000001) return 0.0;
    return (log(v)/log(2.0));
}


functional_product::functional_product(const functional* f_1, const functional* f_2){
    f1=f_1;
    f2=f_2;
}
double functional_product::operator()(double x) const{
    double out_val = (((*f1)(x))*((*f2)(x)));
    return out_val;
}

//****************************************************************
#pragma optimize( "", off )
KahanAccumulation KahanSum(KahanAccumulation accumulation, double value)
{
    KahanAccumulation result;
    double y = value - accumulation.correction;
    double t = accumulation.sum + y;
    result.correction = (t - accumulation.sum) - y;
    result.sum = t;
    return result;
}
#pragma optimize( "", on )

double get_sum(vector<double> arr){
    KahanAccumulation init = {0};
    KahanAccumulation result = accumulate(arr.begin(), arr.end(), init, KahanSum);
    return result.sum;
}

double integral(double lb, double ub, int num_div, const functional &func){
    double len = ub-lb;
    double step_size = len/(double)num_div;
    double result=0.0;
    double vals[num_div+1];
    double x;
    vector<double> results;
    for(int i=0; i<num_div+1; i++){
        x=lb+(double)i*step_size;
        vals[i]=func(x);
    }
    for(int i=0; i<num_div; i++){
        results.push_back((vals[i]+vals[i+1])*step_size/2.0);
    }
    return get_sum(results);
}

double getDivergence(const shape_distribution &p1, const shape_distribution &p2){
    functional_sum_div_2 sum_p_div_2(&p1, &p2);
    log_2_functional log_sum_p_div_2(&sum_p_div_2);
    functional_product arg1(&sum_p_div_2, &log_sum_p_div_2);
    log_2_functional log_p1(&p1);
    functional_product arg2(&p1, &log_p1);
    log_2_functional log_p2(&p2);
    functional_product arg3(&p2, &log_p2);
    double lb = -2000;
    double ub = 2000;
    double num_div = 10000;

    double r1 = -integral(lb, ub, num_div, arg1);
    double r2 = -integral(lb, ub, num_div, arg2);
    double r3 = -integral(lb, ub, num_div, arg3);

    return fabs(r1-((r2+r3)/2.0));
}
