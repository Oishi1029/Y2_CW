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


# Function to set axis scaling
def set_axis_scale():
    print("\nChoose the axis scaling:")
    print("1. Linear scale")
    print("2. Log-log scale")
    print("3. dB scale")
    print("4. Semi-log (horizontal log scale)")
    scale_choice = int(input("Enter your choice (1-4): "))
    if scale_choice == 1:
        plt.xscale("linear")
        plt.yscale("linear")
    elif scale_choice == 2:
        plt.xscale("log")
        plt.yscale("log")
    elif scale_choice == 3:
        plt.yscale("log")
    elif scale_choice == 4:
        plt.xscale("log")


# Main function
def main():
    graphs = []
    superpose = []

    # Input the number of graphs
    num_graphs = int(input("How many graphs do you want to plot? "))

    for i in range(num_graphs):
        print(f"\nGraph {i + 1}:")
        print("1. Use data from a text file")
        print("2. Generate theoretical data")
        graph_type = int(input("Enter your choice (1 or 2): "))

        if graph_type == 1:
            file_path = input("Enter the full file path: ").strip()
            if os.path.exists(file_path):
                print("\nChoose the format:")
                print("1. FFT")
                print("2. Normal")
                graph_format = int(input("Enter your choice (1 or 2): "))
                if graph_format == 1:
                    data = read_fft_file(file_path)
                    if data is not None:
                        freq, db, phase = data.T
                        graphs.append(('fft', freq, db, "Frequency (Hz)", "Amplitude (V)"))
                    else:
                        print("Failed to read FFT file data.")
                elif graph_format == 2:
                    data = read_normal_file(file_path)
                    if data is not None:
                        time, voltage = data.T
                        graphs.append(('normal', time, voltage, "Time (s)", "Voltage (V)"))
                    else:
                        print("Failed to read normal graph file data.")
                else:
                    print("Invalid format. Skipping graph.")
            else:
                print("File does not exist.")

        elif graph_type == 2:
            print("\nSelect section:")
            print("1. FFT")
            print("2. Impulse")
            print("3. Convolution")
            section = int(input("Enter your choice (1-3): "))
            equation = input("Enter the equation (e.g., 'np.sin(2*np.pi*x)'): ").strip()
            x_range = input("Enter the x range as 'start, end' (e.g., '0, 10'): ").strip()
            x_start, x_end = map(float, x_range.split(','))
            x, y = generate_theoretical_data(equation, (x_start, x_end))
            if x is not None:
                graphs.append(('equation', x, y, "Time (s)", "Voltage (V)"))
            else:
                print("Failed to generate theoretical data.")
        else:
            print("Invalid input. Skipping graph.")

    # Superpose graphs
    if input("Do you want to superpose graphs? (yes/no): ").strip().lower() == 'yes':
        indices = input("Enter the graph indices to superpose, separated by commas (e.g., '0,1'): ").strip()
        superpose = [int(idx) for idx in indices.split(',')]

    # Plot graphs
    for i, graph in enumerate(graphs):
        plt.figure(figsize=(10, 6))
        plt.plot(graph[1], graph[2], label=f'Graph {i + 1}')
        plt.xlabel(graph[3])
        plt.ylabel(graph[4])
        set_axis_scale()
        plt.legend()
        plt.title(f"Graph {i + 1}")
        plt.grid(True)
        plt.show()

    # Plot superposed graphs
    if superpose:
        plt.figure(figsize=(10, 6))
        for idx in superpose:
            if idx < len(graphs):
                graph = graphs[idx]
                plt.plot(graph[1], graph[2], label=f'Graph {idx + 1}')
        set_axis_scale()
        plt.legend()
        plt.title("Superposed Graphs")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
