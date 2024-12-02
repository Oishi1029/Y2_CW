// Lab3.h
#ifndef LAB3_H
#define LAB3_H

#include <vector>
#include <string>
#include <sstream>  // for ostringstream and stringstream
#include <fstream>  // for ofstream and ifstream

using namespace std;

class Matrix {
private:
    vector<vector<double>> data;
    int rows;
    int cols;

public:
    Matrix(int n, int m);
    void inputMatrix();
    void inputMatrix(char* argv[], int startIdx);
    void inputValue(int i, int j, double value);
    vector<double> solveLinearSystem();
    Matrix inverse();
    void display();  // Keep old display method for backward compatibility

    // New methods
    void print();  // New aesthetic print method
    void set(int m, int n, double x);
    double get(int m, int n);
    void save(string filename);
    void load(string filename);

private:
    double determinant();
    void swapRows(int i, int j);
    Matrix augmentIdentity();
    bool isSquare();
    bool isValidIndex(int m, int n) const;
};

#endif