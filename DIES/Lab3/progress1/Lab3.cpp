// Lab3.cpp
#include "Lab3.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdexcept>

Matrix::Matrix(int n, int m) : rows(n), cols(m) {
    data.resize(n, vector<double>(m, 0.0));
}

void Matrix::inputMatrix() {
    cout << "Enter the matrix elements row by row:\n";
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cout << "Enter element [" << i << "][" << j << "]: ";
            cin >> data[i][j];
        }
    }
}

void Matrix::inputMatrix(char* argv[], int startIdx) {
    int idx = startIdx;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            data[i][j] = stod(argv[idx++]);
        }
    }
}

void Matrix::display() {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cout << fixed << setprecision(2) << setw(8) << data[i][j] << " ";
        }
        cout << endl;
    }
}

vector<double> Matrix::solveLinearSystem() {
    if (cols != rows + 1) {
        throw runtime_error("Matrix must have n rows and n+1 columns for system solving");
    }

    vector<vector<double>> augmented = data;
    int n = rows;

    // Gaussian elimination
    for (int i = 0; i < n; i++) {
        // Find pivot
        int maxRow = i;
        for (int k = i + 1; k < n; k++) {
            if (abs(augmented[k][i]) > abs(augmented[maxRow][i])) {
                maxRow = k;
            }
        }

        // Swap maximum row with current row
        if (maxRow != i) {
            swap(augmented[i], augmented[maxRow]);
        }

        // Make all rows below this one 0 in current column
        for (int k = i + 1; k < n; k++) {
            double factor = augmented[k][i] / augmented[i][i];
            for (int j = i; j <= n; j++) {
                augmented[k][j] -= factor * augmented[i][j];
            }
        }
    }

    // Back substitution
    vector<double> solution(n);
    for (int i = n - 1; i >= 0; i--) {
        solution[i] = augmented[i][n];
        for (int j = i + 1; j < n; j++) {
            solution[i] -= augmented[i][j] * solution[j];
        }
        solution[i] /= augmented[i][i];
    }

    return solution;
}

bool Matrix::isSquare() {
    return rows == cols;
}

Matrix Matrix::augmentIdentity() {
    if (!isSquare()) {
        throw runtime_error("Matrix must be square for inversion");
    }

    Matrix augmented(rows, 2 * cols);

    // Copy original matrix
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            augmented.data[i][j] = data[i][j];
        }
    }

    // Add identity matrix
    for (int i = 0; i < rows; i++) {
        augmented.data[i][i + cols] = 1.0;
    }

    return augmented;
}

Matrix Matrix::inverse() {
    if (!isSquare()) {
        throw runtime_error("Matrix must be square for inversion");
    }

    Matrix augmented = augmentIdentity();

    // Gaussian elimination
    for (int i = 0; i < rows; i++) {
        // Find pivot
        int maxRow = i;
        for (int k = i + 1; k < rows; k++) {
            if (abs(augmented.data[k][i]) > abs(augmented.data[maxRow][i])) {
                maxRow = k;
            }
        }

        if (abs(augmented.data[maxRow][i]) < 1e-10) {
            throw runtime_error("Matrix is singular, cannot find inverse");
        }

        // Swap maximum row with current row
        if (maxRow != i) {
            swap(augmented.data[i], augmented.data[maxRow]);
        }

        // Scale current row
        double scale = augmented.data[i][i];
        for (int j = i; j < 2 * cols; j++) {
            augmented.data[i][j] /= scale;
        }

        // Eliminate column
        for (int k = 0; k < rows; k++) {
            if (k != i) {
                double factor = augmented.data[k][i];
                for (int j = i; j < 2 * cols; j++) {
                    augmented.data[k][j] -= factor * augmented.data[i][j];
                }
            }
        }
    }

    // Extract inverse matrix
    Matrix inverse(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            inverse.data[i][j] = augmented.data[i][j + cols];
        }
    }

    return inverse;
}

// Add this method to Lab3.cpp
void Matrix::inputValue(int i, int j, double value) {
    if (i >= 0 && i < rows && j >= 0 && j < cols) {
        data[i][j] = value;
    }
}

void Matrix::print() {
    int maxWidth = 0;

    // Find the maximum width needed
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            ostringstream ss;
            ss << fixed << setprecision(6) << data[i][j];
            maxWidth = max(maxWidth, static_cast<int>(ss.str().length()));
        }
    }

    // Print the matrix with aligned columns
    cout << "\n";
    for (int i = 0; i < rows; i++) {
        cout << "│";
        for (int j = 0; j < cols; j++) {
            cout << setw(maxWidth + 2) << fixed << setprecision(6) << data[i][j];
        }
        cout << " │\n";
    }
    cout << "\n";
}

bool Matrix::isValidIndex(int m, int n) const {
    return m >= 0 && m < rows && n >= 0 && n < cols;
}

void Matrix::set(int m, int n, double x) {
    if (!isValidIndex(m, n)) {
        throw out_of_range("Matrix indices out of range");
    }
    data[m][n] = x;
}

double Matrix::get(int m, int n) {
    if (!isValidIndex(m, n)) {
        throw out_of_range("Matrix indices out of range");
    }
    return data[m][n];
}

void Matrix::save(string filename) {
    ofstream outFile(filename);
    if (!outFile) {
        throw runtime_error("Unable to open file for writing: " + filename);
    }

    // Write in MATLAB/Octave ASCII format
    // Each row on a new line, elements separated by spaces
    outFile << scientific << setprecision(16);

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            outFile << data[i][j];
            if (j < cols - 1) outFile << " ";
        }
        outFile << "\n";
    }

    outFile.close();
    if (!outFile) {
        throw runtime_error("Error occurred while writing to file: " + filename);
    }
}

void Matrix::load(string filename) {
    ifstream inFile(filename);
    if (!inFile) {
        throw runtime_error("Unable to open file: " + filename);
    }

    vector<vector<double>> tempData;
    string line;
    int numCols = -1;

    while (getline(inFile, line)) {
        // Skip empty lines
        if (line.empty()) continue;

        vector<double> row;
        stringstream ss(line);
        double value;

        while (ss >> value) {
            row.push_back(value);
        }

        // Verify consistency of number of columns
        if (numCols == -1) {
            numCols = row.size();
        } else if (numCols != static_cast<int>(row.size())) {
            throw runtime_error("Inconsistent number of columns in file: " + filename);
        }

        tempData.push_back(row);
    }

    if (tempData.empty()) {
        throw runtime_error("No data found in file: " + filename);
    }

    // Update matrix dimensions and data
    rows = tempData.size();
    cols = tempData[0].size();
    data = tempData;
}