import numpy as np
import matplotlib.pyplot as plt
import os


# Function to read LTSpice data
# Function to read LTSpice data
def read_ltspice_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        data = []
        for line in lines:
            if line.strip() and not line.startswith('Freq.'):  # Skip empty lines and header
                split_line = line.split()
                freq = float(split_line[0])
                # Split and process the dB and phase values
                db, phase = split_line[1][1:-1].split(',')
                db = float(db[:-2])  # Remove "dB" and convert to float
                phase = float(phase[:-1])  # Remove "°" and convert to float
                data.append((freq, db, phase))
        return np.array(data)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None



# Function to generate theoretical data
def generate_theoretical_data(equation, x_range):
    try:
        x = np.linspace(*x_range, 1000)
        y = eval(equation)
        return x, y
    except Exception as e:
        print(f"Error in equation: {e}")
        return None, None


# Main function
def main():
    graphs = []
    superpose = []

    # Input the number of graphs
    num_graphs = int(input("How many graphs do you want to plot? "))

    for i in range(num_graphs):
        print(f"Graph {i + 1}:")
        graph_type = input(
            "Enter 'file' to use data from a text file or 'equation' for theoretical data: ").strip().lower()

        if graph_type == 'file':
            file_path = input("Enter the full file path: ").strip()
            if os.path.exists(file_path):
                data = read_ltspice_file(file_path)
                if data is not None:
                    freq, db, phase = data.T
                    graphs.append(('file', freq, db, phase))
                else:
                    print("Failed to read file data.")
            else:
                print("File does not exist.")

        elif graph_type == 'equation':
            section = input("Select section (1: FFT, 2: Impulse, 3: Convolution): ").strip()
            equation = input("Enter the equation (e.g., 'np.sin(2*np.pi*x)'): ").strip()
            x_range = input("Enter the x range as 'start, end' (e.g., '0, 10'): ").strip()
            x_start, x_end = map(float, x_range.split(','))
            x, y = generate_theoretical_data(equation, (x_start, x_end))
            if x is not None:
                graphs.append(('equation', x, y, section))
            else:
                print("Failed to generate theoretical data.")

        else:
            print("Invalid input. Skipping graph.")

    # Superpose graphs
    if input("Do you want to superpose graphs? (yes/no): ").strip().lower() == 'yes':
        indices = input("Enter the graph indices to superpose, separated by commas (e.g., '0,1'): ").strip()
        superpose = [int(idx) for idx in indices.split(',')]

    # Plot graphs
    plt.figure(figsize=(10, 6))
    for i, graph in enumerate(graphs):
        if graph[0] == 'file':
            plt.plot(graph[1], graph[2], label=f'Graph {i + 1} (File)')
        elif graph[0] == 'equation':
            plt.plot(graph[1], graph[2], label=f'Graph {i + 1} (Equation, Section {graph[3]})')

    if superpose:
        plt.figure(figsize=(10, 6))
        for idx in superpose:
            graph = graphs[idx]
            if graph[0] == 'file':
                plt.plot(graph[1], graph[2], label=f'Graph {idx + 1} (File)')
            elif graph[0] == 'equation':
                plt.plot(graph[1], graph[2], label=f'Graph {idx + 1} (Equation, Section {graph[3]})')
        plt.legend()
        plt.title("Superposed Graph")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid(True)
        plt.show()

    # Show all individual graphs
    plt.legend()
    plt.title("All Graphs")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
