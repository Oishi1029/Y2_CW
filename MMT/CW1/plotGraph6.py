import numpy as np
import matplotlib.pyplot as plt
import os


def read_fft_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        data = []
        for line in lines[1:]:
            if line.strip():
                split_line = line.split()
                freq = float(split_line[0])
                db, phase = split_line[1][1:-1].split(',')
                db = float(db[:-2])
                phase = float(phase[:-1])
                data.append((freq, db, phase))
        return np.array(data)
    except Exception as e:
        print(f"Error reading FFT file: {e}")
        return None


def read_normal_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        data = []
        for line in lines[1:]:
            if line.strip():
                split_line = line.split()
                time = float(split_line[0])
                voltage = float(split_line[1])
                data.append((time, voltage))
        return np.array(data)
    except Exception as e:
        print(f"Error reading normal graph file: {e}")
        return None


def generate_equation_data(equation, x_range):
    try:
        x = np.linspace(*x_range, 1000)
        y = eval(equation)
        return x, y
    except Exception as e:
        print(f"Error in equation: {e}")
        return None, None


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


def are_compatible_types(type1, type2):
    fft_types = {'fft', 'fft equation'}
    normal_types = {'normal', 'normal equation'}

    return (type1 in fft_types and type2 in fft_types) or \
        (type1 in normal_types and type2 in normal_types)


def main():
    graphs = []

    num_graphs = int(input("How many graphs do you want to plot? "))

    for i in range(num_graphs):
        print(f"\nGraph {i + 1}:")
        print("1. Use data from a text file")
        print("2. Use a mathematical equation")
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
                        graphs.append(('fft', file_path, freq, db, "Frequency (Hz)", "Amplitude (V)"))
                    else:
                        print("Failed to read FFT file data.")
                elif graph_format == 2:
                    data = read_normal_file(file_path)
                    if data is not None:
                        time, voltage = data.T
                        graphs.append(('normal', file_path, time, voltage, "Time (s)", "Voltage (V)"))
                    else:
                        print("Failed to read normal graph file data.")
                else:
                    print("Invalid format. Skipping graph.")
            else:
                print("File does not exist.")

        elif graph_type == 2:
            print("\nChoose the type of equation:")
            print("1. FFT Equation")
            print("2. Normal Equation")
            equation_type = int(input("Enter your choice (1 or 2): "))
            equation = input("Enter the equation (e.g., 'np.sin(2*np.pi*x)'): ").strip()
            x_range = input("Enter the x range as 'start, end' (e.g., '0, 10'): ").strip()
            x_start, x_end = map(float, x_range.split(','))
            x, y = generate_equation_data(equation, (x_start, x_end))
            if x is not None:
                if equation_type == 1:
                    graphs.append(('fft equation', "Equation", x, y, "Frequency (Hz)", "Amplitude (V)"))
                elif equation_type == 2:
                    graphs.append(('normal equation', "Equation", x, y, "Time (s)", "Voltage (V)"))
                else:
                    print("Invalid equation type.")
            else:
                print("Failed to generate data from equation.")

    # Plot handling
    if input("\nDo you want to superpose graphs? (yes/no): ").strip().lower() == 'yes':
        print("\nAvailable graphs:")
        for idx, (gtype, fname, _, _, _, _) in enumerate(graphs):
            print(f"{idx}: {gtype.upper()} - {fname}")

        superpose_indices = input("Enter the graph indices to superpose, separated by commas (e.g., '0,1'): ").strip()
        superpose_indices = [int(idx) for idx in superpose_indices.split(',')]

        # Check compatibility of graph types
        types = [graphs[idx][0] for idx in superpose_indices]
        compatible = all(are_compatible_types(types[0], t) for t in types[1:])

        if compatible:
            plt.figure(figsize=(10, 6))
            for idx in superpose_indices:
                graph = graphs[idx]
                plt.plot(graph[2], graph[3], label=f"{graph[1]} ({graph[0].upper()})")
            plt.xlabel(graphs[superpose_indices[0]][4])
            plt.ylabel(graphs[superpose_indices[0]][5])
            print("\nSetting axis scaling for the graph:")
            set_axis_scale()
            plt.legend()
            plt.title("Superposed Graphs")
            plt.grid(True)
            plt.show()
        else:
            print("Cannot superpose these graphs. Please choose compatible graph types:")
            print("- FFT graphs can be superposed with FFT equation graphs")
            print("- Normal graphs can be superposed with Normal equation graphs")
    else:
        # Plot individual graphs only if not superposing
        for i, graph in enumerate(graphs):
            plt.figure(figsize=(10, 6))
            plt.plot(graph[2], graph[3], label=f"{graph[1]} ({graph[0].upper()})")
            plt.xlabel(graph[4])
            plt.ylabel(graph[5])
            print(f"\nSetting axis scaling for Graph {i + 1}:")
            set_axis_scale()
            plt.legend()
            plt.title(f"Graph {i + 1}")
            plt.grid(True)
            plt.show()


if __name__ == "__main__":
    main()
