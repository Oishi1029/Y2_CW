// main.cpp
#include "Lab3.h"
#include <iostream>
#include <string>
#include <sstream>
#include <limits>

void printUsage() {
    cout << "Usage:\n";
    cout << "1. Command line input: program_name matrix_elements\n";
    cout << "   Example: program_name 1 2 3 4 5 6\n";
    cout << "2. Standard input: just run the program\n";
}

void printMenu() {
    cout << "\nMatrix Operations Menu:\n";
    cout << "1. Solve system of linear equations\n";
    cout << "2. Find inverse matrix\n";
    cout << "3. Print matrix\n";
    cout << "4. Set specific element\n";
    cout << "5. Get specific element\n";
    cout << "6. Save matrix to file\n";
    cout << "7. Load matrix from file\n";
    cout << "8. Exit\n";
    cout << "Enter choice (1-8): ";
}

bool validateDimensions(int rows, int cols, int operation) {
    if (operation == 1 && cols != rows + 1) {
        cout << "For system solving, columns must be rows + 1\n";
        return false;
    }
    if (operation == 2 && cols != rows) {
        cout << "For inverse, matrix must be square\n";
        return false;
    }
    return true;
}

void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void processMatrixOperation(Matrix& mat, int operation) {
    try {
        switch (operation) {
            case 1: { // Solve system
                vector<double> solution = mat.solveLinearSystem();
                cout << "\nSolution:\n";
                for (int i = 0; i < solution.size(); i++) {
                    cout << "x" << i + 1 << " = " << solution[i] << endl;
                }
                break;
            }
            case 2: { // Inverse
                Matrix inverse = mat.inverse();
                cout << "\nInverse Matrix:\n";
                inverse.print();
                break;
            }
            case 3: { // Print
                cout << "\nCurrent Matrix:\n";
                mat.print();
                break;
            }
            case 4: { // Set element
                int m, n;
                double value;
                cout << "Enter row index: ";
                cin >> m;
                cout << "Enter column index: ";
                cin >> n;
                cout << "Enter value: ";
                cin >> value;
                mat.set(m, n, value);
                cout << "Element updated successfully.\n";
                break;
            }
            case 5: { // Get element
                int m, n;
                cout << "Enter row index: ";
                cin >> m;
                cout << "Enter column index: ";
                cin >> n;
                double value = mat.get(m, n);
                cout << "Value at (" << m << "," << n << ") = " << value << endl;
                break;
            }
            case 6: { // Save
                string filename;
                cout << "Enter filename to save: ";
                clearInputBuffer();
                getline(cin, filename);
                mat.save(filename);
                cout << "Matrix saved successfully to " << filename << endl;
                break;
            }
            case 7: { // Load
                string filename;
                cout << "Enter filename to load: ";
                clearInputBuffer();
                getline(cin, filename);
                mat.load(filename);
                cout << "Matrix loaded successfully from " << filename << endl;
                cout << "Loaded matrix:\n";
                mat.print();
                break;
            }
        }
    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }
}

int main(int argc, char* argv[]) {
    int rows, cols;
    vector<double> input_values;

    // Get matrix dimensions
    cout << "Enter number of rows: ";
    cin >> rows;
    cout << "Enter number of columns: ";
    cin >> cols;

    Matrix mat(rows, cols);

    if (argc > 1) {  // Command line matrix input
        for (int i = 1; i < argc; i++) {
            try {
                input_values.push_back(stod(argv[i]));
            } catch (const invalid_argument& e) {
                cout << "Invalid number format in command line arguments\n";
                return 1;
            }
        }

        if (input_values.size() != rows * cols) {
            cout << "Error: Number of input values (" << input_values.size()
                 << ") does not match matrix dimensions (" << rows << "x" << cols
                 << " = " << rows * cols << ")\n";
            return 1;
        }

        int idx = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                mat.inputValue(i, j, input_values[idx++]);
            }
        }
    } else {  // Standard input for matrix
        mat.inputMatrix();
    }

    // Operation menu loop
    int operation;
    do {
        printMenu();
        cin >> operation;

        if (operation < 1 || operation > 8) {
            cout << "Invalid option. Please try again.\n";
            continue;
        }

        if (operation == 8) {
            cout << "Exiting program.\n";
            break;
        }

        // Validate dimensions for specific operations
        if ((operation == 1 || operation == 2) && !validateDimensions(rows, cols, operation)) {
            continue;
        }

        processMatrixOperation(mat, operation);

    } while (true);

    return 0;
}