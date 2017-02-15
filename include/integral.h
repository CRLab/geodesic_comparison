#ifndef INTEGRAL_H
#define INTEGRAL_H

#include <stdlib.h>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <fstream>
#include <cstring>
#include <numeric>

#define PI 3.1415926535897

using namespace std;

//functions for getting median of list
bool sort_l2h(double i, double j);
double getMedian(vector<double> vec);
//gaussian kernel
double K(double x);

//abstract class for function input for integral
class functional{
public:
    functional(){}
    virtual ~functional(){}
    virtual double operator()(double x) const = 0;
};


class shape_distribution: public functional{
private:
    vector<double> global_geodesic;

public:
    double h;
    shape_distribution(const char* filename);
    virtual double operator()(double x) const;
};

class functional_sum_div_2: public functional{
private:
    const functional* f1;
    const functional* f2;
public:
    functional_sum_div_2(const functional* f_1, const functional* f_2);
    virtual double operator()(double x) const;
};

class log_2_functional: public functional{
private:
    const functional* f;
public:
    log_2_functional(const functional* f_);
    virtual double operator()(double x) const;
};

class functional_product: public functional{
private:
    const functional* f1;
    const functional* f2;
public:
    functional_product(const functional* f_1, const functional* f_2);
    virtual double operator()(double x) const;
};

//****************************************************************
//Kahan vector accumulation method
struct KahanAccumulation
{
    double sum;
    double correction;
};
KahanAccumulation KahanSum(KahanAccumulation accumulation, double value);
double get_sum(vector<double> arr);

//method for performing integration on functions
double integral(double lb, double ub, int num_div, const functional &func);

//compare two shape distributions by Jenson-Shannon Divergence
double getDivergence(const shape_distribution &p1, const shape_distribution &p2);

#endif
