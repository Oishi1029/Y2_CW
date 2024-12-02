// main.cpp
#include "Lab3.h"
#include <iostream>
#include <string>
#include <map>
#include <cctype>
#include <limits>

void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void printMainMenu() {
    cout << "\nMain Menu:\n";
    cout << "1. Create new matrix\n";
    cout << "2. Perform operations on existing matrix\n";
    cout << "3. List all matrices\n";
    cout << "4. Delete matrix\n";
    cout << "5. Exit\n";
    cout << "Enter choice (1-5): ";
}

void printOperationMenu() {
    cout << "\nMatrix Operations Menu:\n";
    cout << "1. Solve system of linear equations\n";
    cout << "2. Find inverse matrix\n";
    cout << "3. Print matrix\n";
    cout << "4. Set specific element\n";
    cout << "5. Get specific element\n";
    cout << "6. Save matrix to file\n";
    cout << "7. Load matrix from file\n";
    cout << "8. Return to main menu\n";
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

void listMatrices(const map<char, Matrix>& matrices) {
    cout << "\nExisting matrices:\n";
    if (matrices.empty()) {
        cout << "No matrices created yet.\n";
        return;
    }
    for (const auto& pair : matrices) {
        cout << "Matrix " << pair.first << " ("
             << pair.second.getRows() << "x"
             << pair.second.getCols() << ")\n";
    }
}

char getMatrixLabel() {
    char label;
    do {
        cout << "Enter matrix label (A-Z): ";
        cin >> label;
        label = toupper(label);
        clearInputBuffer();

        if (label < 'A' || label > 'Z') {
            cout << "Invalid label. Please use letters A-Z.\n";
            continue;
        }
        break;
    } while (true);
    return label;
}

void processMatrixOperation(Matrix& mat, int operation) {
    try {
        switch (operation) {
            case 1: { // Solve system
                if (!validateDimensions(mat.getRows(), mat.getCols(), 1)) return;
                vector<double> solution = mat.solveLinearSystem();
                cout << "\nSolution:\n";
                for (size_t i = 0; i < solution.size(); i++) {
                    cout << "x" << i + 1 << " = " << solution[i] << endl;
                }
                break;
            }
            case 2: { // Inverse
                if (!validateDimensions(mat.getRows(), mat.getCols(), 2)) return;
                Matrix inverse = mat.inverse();
                cout << "\nInverse Matrix:\n";
                inverse.print();
                break;
            }
            case 3: { // Print
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
                mat.print();
                break;
            }
        }
    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }
}

int main() {
    map<char, Matrix> matrices;
    int choice;

    do {
        printMainMenu();
        cin >> choice;
        clearInputBuffer();

        switch (choice) {
            case 1: { // Create new matrix
                char label = getMatrixLabel();

                if (matrices.find(label) != matrices.end()) {
                    cout << "Matrix " << label << " already exists. Overwrite? (y/n): ";
                    char confirm;
                    cin >> confirm;
                    if (tolower(confirm) != 'y') continue;
                }

                int rows, cols;
                cout << "Enter number of rows: ";
                cin >> rows;
                cout << "Enter number of columns: ";
                cin >> cols;

                matrices[label] = Matrix(rows, cols);
                cout << "Enter matrix elements:\n";
                matrices[label].inputMatrix();
                cout << "Matrix " << label << " created successfully.\n";
                break;
            }
            case 2: { // Perform operations
                if (matrices.empty()) {
                    cout << "No matrices available. Please create a matrix first.\n";
                    continue;
                }

                listMatrices(matrices);
                char label = getMatrixLabel();

                if (matrices.find(label) == matrices.end()) {
                    cout << "Matrix " << label << " does not exist.\n";
                    continue;
                }

                int operation;
                do {
                    printOperationMenu();
                    cin >> operation;

                    if (operation == 8) break;
                    if (operation < 1 || operation > 8) {
                        cout << "Invalid option. Please try again.\n";
                        continue;
                    }

                    processMatrixOperation(matrices[label], operation);
                } while (true);
                break;
            }
            case 3: { // List matrices
                listMatrices(matrices);
                break;
            }
            case 4: { // Delete matrix
                if (matrices.empty()) {
                    cout << "No matrices to delete.\n";
                    continue;
                }

                listMatrices(matrices);
                char label = getMatrixLabel();

                if (matrices.find(label) == matrices.end()) {
                    cout << "Matrix " << label << " does not exist.\n";
                    continue;
                }

                matrices.erase(label);
                cout << "Matrix " << label << " deleted successfully.\n";
                break;
            }
            case 5: { // Exit
                cout << "Exiting program.\n";
                break;
            }
            default:
                cout << "Invalid choice. Please try again.\n";
        }
    } while (choice != 5);

    return 0;
}