#include <iostream>
#include <cmath>

class ElectricalCircuit {
private:
    double V;     // Voltage in volts
    double Ri;    // Internal resistance in ohms
    double Rt;    // Transmission line resistance in ohms
    double PL;    // Power delivered to the load in watts
    double I;     // Current in amperes (unknown)
    double RL;    // Load resistance in ohms (unknown)

public:
    // Constructor
    ElectricalCircuit(double voltage = 12.0, double internalResistance = 1.0, double transmissionResistance = 1.0, double powerLoad = 10.0)
        : V(voltage), Ri(internalResistance), Rt(transmissionResistance), PL(powerLoad), I(0.0), RL(0.0) {}

    // Destructor
    ~ElectricalCircuit() {
        std::cout << "ElectricalCircuit object destroyed.\n";
    }

    // Accessor methods
    double getVoltage() const { return V; }
    double getInternalResistance() const { return Ri; }
    double getTransmissionResistance() const { return Rt; }
    double getPowerLoad() const { return PL; }
    double getCurrent() const { return I; }
    double getLoadResistance() const { return RL; }

    // Mutator methods
    void setVoltage(double voltage) { V = voltage; }
    void setInternalResistance(double resistance) { Ri = resistance; }
    void setTransmissionResistance(double resistance) { Rt = resistance; }
    void setPowerLoad(double power) { PL = power; }

    // Function to compute the unknowns: Current (I) and Load Resistance (RL)
    void simulate() {
        RL = (V * V) / PL; // Calculate RL from the given power and voltage
        double totalResistance = Ri + Rt + RL;
        I = V / totalResistance; // Calculate I using Ohm's Law
    }

    // Function to display the results
    void displayResults() const {
        std::cout << "Simulation Results:\n";
        std::cout << "Load Resistance (RL): " << RL << " ohms\n";
        std::cout << "Current (I): " << I << " amperes\n";
    }
};

int main() {
    double V, Ri, Rt, PL;

    // User input for parameters
    std::cout << "Enter the battery voltage (V) in volts: ";
    std::cin >> V;
    std::cout << "Enter the internal resistance (Ri) in ohms: ";
    std::cin >> Ri;
    std::cout << "Enter the transmission line resistance (Rt) in ohms: ";
    std::cin >> Rt;
    std::cout << "Enter the power delivered to the load (PL) in watts: ";
    std::cin >> PL;

    // Create an ElectricalCircuit object
    ElectricalCircuit circuit(V, Ri, Rt, PL);

    // Run simulation
    circuit.simulate();

    // Display results
    circuit.displayResults();

    return 0;
}
