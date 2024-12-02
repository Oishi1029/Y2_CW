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
    Matrix() : rows(0), cols(0) {} // Default constructor
    Matrix(int n, int m);
    void inputMatrix();
    void inputMatrix(char* argv[], int startIdx);
    void inputValue(int i, int j, double value);
    vector<double> solveLinearSystem();
    Matrix inverse();
    void print();
    void set(int m, int n, double x);
    double get(int m, int n);
    void save(string filename);
    void load(string filename);
    bool isEmpty() const { return rows == 0 || cols == 0; }
    int getRows() const { return rows; }
    int getCols() const { return cols; }
    void resize(int n, int m);
    void display();

private:
    double determinant();
    void swapRows(int i, int j);
    Matrix augmentIdentity();
    bool isSquare();
    bool isValidIndex(int m, int n) const;
};

#endif