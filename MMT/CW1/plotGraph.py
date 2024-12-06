import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os


class DataPlotter:
    def __init__(self):
        self.graphs = []  # List to store all graph data
        self.graph_types = []  # List to store whether each graph is from file or equation
        self.graph_names = []  # List to store names of graphs

    def read_data(self, filename):
        """Read data from text file"""
        try:
            # Try reading with tab delimiter first
            data = pd.read_csv(filename, delimiter='\t', skipinitialspace=True)
            # If only one column is read, try space delimiter
            if len(data.columns) == 1:
                data = pd.read_csv(filename, delimiter=r'\s+', skipinitialspace=True)

            # Set default column names if they're numeric
            if data.columns.str.match(r'^\d+$').all():
                data.columns = [f'Column_{i}' for i in range(len(data.columns))]

            return data

        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def generate_equation_data(self, equation_type):
        """Generate data from predefined equations"""
        x = np.linspace(0, 10, 1000)
        if equation_type == 'sine':
            y = np.sin(x)
            name = 'Sine Wave'
        elif equation_type == 'cosine':
            y = np.cos(x)
            name = 'Cosine Wave'
        elif equation_type == 'exponential':
            y = np.exp(-x / 2)
            name = 'Exponential Decay'
        else:
            return None, None

        return pd.DataFrame({'x': x, 'y': y}), name

    def setup_graphs(self):
        """Interactive setup of graphs"""
        # Get number of graphs
        while True:
            try:
                num_graphs = int(input("How many graphs do you want to plot? "))
                if num_graphs > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

        # Setup each graph
        for i in range(num_graphs):
            print(f"\nGraph {i + 1}:")
            while True:
                graph_type = input("Choose graph type (1: From file, 2: From equation): ").strip()
                if graph_type in ['1', '2']:
                    break
                print("Please enter 1 or 2.")

            if graph_type == '1':
                # File input
                while True:
                    file_path = input("Enter the file path: ").strip()
                    if os.path.exists(file_path):
                        data = self.read_data(file_path)
                        if data is not None:
                            self.graphs.append(data)
                            self.graph_types.append('file')
                            self.graph_names.append(f"Data from {os.path.basename(file_path)}")
                            break
                    print("File not found or invalid. Please try again.")

            else:
                # Equation input
                print("\nAvailable equations:")
                print("1: Sine wave")
                print("2: Cosine wave")
                print("3: Exponential decay")
                while True:
                    eq_choice = input("Choose equation (1-3): ").strip()
                    if eq_choice in ['1', '2', '3']:
                        eq_type = ['sine', 'cosine', 'exponential'][int(eq_choice) - 1]
                        data, name = self.generate_equation_data(eq_type)
                        if data is not None:
                            self.graphs.append(data)
                            self.graph_types.append('equation')
                            self.graph_names.append(name)
                            break
                    print("Please enter a valid choice (1-3).")

    def setup_plot_configuration(self):
        """Get plot configuration from user"""
        # Ask about superposing graphs
        while True:
            superpose = input("\nDo you want to superpose graphs? (y/n): ").strip().lower()
            if superpose in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'.")

        if superpose == 'y':
            # Get graphs to superpose
            print("\nAvailable graphs:")
            for i, name in enumerate(self.graph_names):
                print(f"{i + 1}: {name}")

            while True:
                try:
                    indices = input("Enter graph numbers to superpose (comma-separated, e.g., 1,2): ").strip()
                    indices = [int(i) - 1 for i in indices.split(',')]
                    if all(0 <= i < len(self.graphs) for i in indices):
                        break
                    print("Please enter valid graph numbers.")
                except ValueError:
                    print("Please enter valid numbers.")

            return True, indices

        return False, None

    def plot_graphs(self):
        """Plot graphs based on user configuration"""
        superpose, superpose_indices = self.setup_plot_configuration()

        if superpose:
            # Create single plot with superposed graphs
            plt.figure(figsize=(12, 8))
            for idx in superpose_indices:
                data = self.graphs[idx]
                if self.graph_types[idx] == 'file':
                    plt.plot(data[data.columns[0]], data[data.columns[1]],
                             label=self.graph_names[idx])
                else:
                    plt.plot(data['x'], data['y'], label=self.graph_names[idx])

            plt.grid(True)
            plt.legend()
            plt.title("Superposed Graphs")

        else:
            # Create separate plots
            num_graphs = len(self.graphs)
            rows = int(np.ceil(np.sqrt(num_graphs)))
            cols = int(np.ceil(num_graphs / rows))

            fig = plt.figure(figsize=(6 * cols, 5 * rows))

            for i, (data, graph_type, name) in enumerate(zip(self.graphs, self.graph_types, self.graph_names)):
                ax = plt.subplot(rows, cols, i + 1)
                if graph_type == 'file':
                    ax.plot(data[data.columns[0]], data[data.columns[1]])
                else:
                    ax.plot(data['x'], data['y'])
                ax.set_title(name)
                ax.grid(True)

            plt.tight_layout()

        plt.show()


def main():
    plotter = DataPlotter()
    plotter.setup_graphs()
    plotter.plot_graphs()


if __name__ == "__main__":
    main()
