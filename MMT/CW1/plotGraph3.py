import numpy as np
import matplotlib.pyplot as plt
import os


# Function to read FFT data from a text file
def read_fft_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Skip the first row (header)
        data = []
        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                split_line = line.split()
                freq = float(split_line[0])
                db, phase = split_line[1][1:-1].split(',')
                db = float(db[:-2])  # Remove "dB" and convert to float
                phase = float(phase[:-1])  # Remove "°" and convert to float
                data.append((freq, db, phase))
        return np.array(data)
    except Exception as e:
        print(f"Error reading FFT file: {e}")
        return None


# Function to read normal graph data from a text file
def read_normal_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Skip the first row (header)
        data = []
        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                split_line = line.split()
                time = float(split_line[0])
                voltage = float(split_line[1])
                data.append((time, voltage))
        return np.array(data)
    except Exception as e:
        print(f"Error reading normal graph file: {e}")
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
        graph_type = input("Enter 'file' to use data from a text file or 'equation' for theoretical data: ").strip().lower()

        if graph_type == 'file':
            file_path = input("Enter the full file path: ").strip()
            if os.path.exists(file_path):
                graph_format = input("Enter the format ('fft' or 'normal'): ").strip().lower()
                if graph_format == 'fft':
                    data = read_fft_file(file_path)
                    if data is not None:
                        freq, db, phase = data.T
                        x_label = input("Enter the label for the horizontal axis: ").strip()
                        y_label = input("Enter the label for the vertical axis: ").strip()
                        graphs.append(('fft', freq, db, phase, x_label, y_label))
                    else:
                        print("Failed to read FFT file data.")
                elif graph_format == 'normal':
                    data = read_normal_file(file_path)
                    if data is not None:
                        time, voltage = data.T
                        x_label = input("Enter the label for the horizontal axis: ").strip()
                        y_label = input("Enter the label for the vertical axis: ").strip()
                        graphs.append(('normal', time, voltage, x_label, y_label))
                    else:
                        print("Failed to read normal graph file data.")
                else:
                    print("Invalid format. Skipping graph.")
            else:
                print("File does not exist.")

        elif graph_type == 'equation':
            section = input("Select section (1: FFT, 2: Impulse, 3: Convolution): ").strip()
            equation = input("Enter the equation (e.g., 'np.sin(2*np.pi*x)'): ").strip()
            x_range = input("Enter the x range as 'start, end' (e.g., '0, 10'): ").strip()
            x_start, x_end = map(float, x_range.split(','))
            x, y = generate_theoretical_data(equation, (x_start, x_end))
            if x is not None:
                x_label = input("Enter the label for the horizontal axis: ").strip()
                y_label = input("Enter the label for the vertical axis: ").strip()
                graphs.append(('equation', x, y, section, x_label, y_label))
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
    plotted_anything = False
    for i, graph in enumerate(graphs):
        if graph[0] == 'fft':
            plt.plot(graph[1], graph[2], label=f'Graph {i + 1} (FFT)')
            plt.xlabel(graph[4])
            plt.ylabel(graph[5])
            plotted_anything = True
        elif graph[0] == 'normal':
            plt.plot(graph[1], graph[2], label=f'Graph {i + 1} (Normal)')
            plt.xlabel(graph[3])
            plt.ylabel(graph[4])
            plotted_anything = True
        elif graph[0] == 'equation':
            plt.plot(graph[1], graph[2], label=f'Graph {i + 1} (Equation, Section {graph[3]})')
            plt.xlabel(graph[4])
            plt.ylabel(graph[5])
            plotted_anything = True

    if plotted_anything:
        plt.legend()
        plt.title("All Graphs")
        plt.grid(True)
        plt.show()
    else:
        print("No graphs to display.")

    if superpose:
        plt.figure(figsize=(10, 6))
        plotted_anything = False  # Track if any graph is plotted
        for idx in superpose:
            if idx < len(graphs):  # Ensure index is valid
                graph = graphs[idx]
                if graph[0] == 'fft':
                    plt.plot(graph[1], graph[2], label=f'Graph {idx + 1} (FFT)')
                    plotted_anything = True
                elif graph[0] == 'normal':
                    plt.plot(graph[1], graph[2], label=f'Graph {idx + 1} (Normal)')
                    plotted_anything = True
                elif graph[0] == 'equation':
                    plt.plot(graph[1], graph[2], label=f'Graph {idx + 1} (Equation, Section {graph[3]})')
                    plotted_anything = True
        if plotted_anything:
            plt.legend()
            plt.title("Superposed Graph")
            plt.grid(True)
            plt.show()
        else:
            print("No graphs to superpose.")

    # Show all individual graphs
    #if any(graphs):  # Ensure there are graphs to display
     #   plt.legend()
    #else:
     #   print("No graphs to display.")

    #plt.legend()
    #plt.title("All Graphs")
    #plt.grid(True)
    #plt.show()


if __name__ == "__main__":
    main()
