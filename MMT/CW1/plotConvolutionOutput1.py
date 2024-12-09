import numpy as np
import matplotlib.pyplot as plt

# Global saved settings
saved_x_min = None
saved_x_max = None
saved_y_min = None
saved_y_max = None


def load_text_file_data(filename):
    """
    Loads convolution output data from a text file.

    Parameters:
        filename (str): Path to the text file containing time and V_o(t) data.

    Returns:
        np.ndarray: Array of time values.
        np.ndarray: Array of V_o(t) values.
    """
    times = []
    V_o = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("time"):
                continue
            parts = line.split()
            if len(parts) < 2:
                print(f"Warning: Skipping invalid data line: {line}")
                continue
            try:
                time = float(parts[0])
                value = float(parts[1])
            except ValueError:
                print(f"Warning: Skipping invalid data line: {line}")
                continue
            times.append(time)
            V_o.append(value)
    return np.array(times), np.array(V_o)


def V_o_theoretical(t):
    """
    Computes the theoretical convolution output V_o(t) based on the piecewise equation.

    Parameters:
        t (np.ndarray): Array of time values.

    Returns:
        np.ndarray: Array of V_o(t) values.
    """
    V_o = np.zeros_like(t)

    # Condition 1: t < 0
    mask1 = t < 0
    V_o[mask1] = 0

    # Condition 2: 0 < t < 1 ms
    mask2 = (t >= 0) & (t < 1e-3)
    V_o[mask2] = 0.5 * np.exp(-10000 * t[mask2])

    # Condition 3: 1 ms ≤ t < 2 ms
    mask3 = (t >= 1e-3) & (t < 2e-3)
    V_o[mask3] = 0.5 * np.exp(-10000 * (t[mask3] - 1e-3)) + 0.5 * np.exp(-10000 * t[mask3])

    # Condition 4: t ≥ 2 ms
    mask4 = t >= 2e-3
    V_o[mask4] = 0.5 * np.exp(-10000 * t[mask4]) * (1 + np.exp(10)) - np.exp(-10000 * (t[mask4] - 2e-3))

    return V_o


def get_yes_no(prompt):
    """
    Utility function to get a yes/no response from the user.

    Parameters:
        prompt (str): The prompt message to display.

    Returns:
        str: 'y' for yes or 'n' for no.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def main():
    global saved_x_min, saved_x_max, saved_y_min, saved_y_max

    # Store loaded text file data in a list for reuse.
    loaded_data_list = []

    while True:
        try:
            num_graphs = int(input("How many convolution output graphs do you want to plot? "))
            if num_graphs <= 0:
                print("Please enter a positive integer for the number of graphs.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        plot_sources = []
        equation_time_specs = []
        any_text_file_used = False

        # Step 1: Gather user input for each graph
        for i in range(num_graphs):
            print(f"\nFor convolution output graph {i + 1}:")
            while True:
                source_type = input("Is this graph from text file (t) or equation (e)? [t/e]: ").strip().lower()
                if source_type in ['t', 'e']:
                    break
                else:
                    print("Invalid input. Please enter 't' for text file or 'e' for equation.")

            if source_type == 't':
                any_text_file_used = True
                # If text file data used before, prompt if user wants to reuse existing data
                if len(loaded_data_list) > 0:
                    print("\nYou have previously loaded text file data:")
                    for idx, d in enumerate(loaded_data_list):
                        print(f"{idx}: {d['filename']}")
                    reuse_choice = get_yes_no("Do you want to reuse previously loaded data? [y/n]: ")
                    if reuse_choice == 'y':
                        while True:
                            try:
                                chosen_idx = int(input(
                                    f"Enter the index of the previously loaded data to use (0 to {len(loaded_data_list) - 1}): "))
                                if 0 <= chosen_idx < len(loaded_data_list):
                                    break
                                else:
                                    print(f"Please enter a number between 0 and {len(loaded_data_list) - 1}.")
                            except ValueError:
                                print("Invalid input. Please enter a valid integer.")
                        plot_sources.append({'type': 'text', 'data_index': chosen_idx})
                        equation_time_specs.append(None)
                        # Assign label
                        default_label = loaded_data_list[chosen_idx]['filename']
                        assign_label = get_yes_no(
                            "Do you want to assign a custom name for the legend of this graph? [y/n]: ")
                        if assign_label == 'y':
                            custom_label = input("Enter legend name: ").strip()
                        else:
                            custom_label = default_label
                        plot_sources[-1]['label'] = custom_label
                        continue

                # If not reusing:
                while True:
                    filename = input("Enter the text file name/path containing convolution output data: ").strip()
                    try:
                        times, V_o = load_text_file_data(filename)
                        if len(times) == 0:
                            print(f"No valid data found in '{filename}'. Please check the file and try again.")
                            continue
                        break
                    except FileNotFoundError:
                        print(f"File '{filename}' not found. Please enter a valid file name/path.")
                    except Exception as e:
                        print(f"An error occurred while loading the file: {e}")
                        print("Please ensure the file is in the correct format and try again.")

                loaded_data_list.append(
                    {'filename': filename, 'times': times, 'V_o': V_o})
                plot_sources.append({'type': 'text', 'data_index': len(loaded_data_list) - 1})
                equation_time_specs.append(None)
                # Assign label
                default_label = filename
                assign_label = get_yes_no("Do you want to assign a custom name for the legend of this graph? [y/n]: ")
                if assign_label == 'y':
                    custom_label = input("Enter legend name: ").strip()
                else:
                    custom_label = default_label
                plot_sources[-1]['label'] = custom_label

            else:
                # Equation based
                custom_choice = get_yes_no(
                    "Do you want to specify time range and sample points for the theoretical convolution output? [y/n]: ")
                if custom_choice == 'y':
                    while True:
                        try:
                            t_min = float(input("Enter minimum time (s): "))
                            t_max_user = float(input("Enter maximum time (s): "))
                            if t_max_user <= t_min:
                                print("Maximum time must be greater than minimum time.")
                                continue
                            num_points = int(input("Enter number of sample points: "))
                            if num_points <= 0:
                                print("Number of sample points must be a positive integer.")
                                continue
                            break
                        except ValueError:
                            print(
                                "Invalid input. Please enter numerical values for times and an integer for sample points.")
                    eq_params = {
                        't_min': t_min,
                        't_max_user': t_max_user,
                        'num_points': num_points,
                        'custom': True
                    }
                else:
                    eq_params = {
                        't_min': -1e-3,  # Start a bit before zero to capture t < 0
                        't_max_user': 5e-3,  # Adjusted default time range based on equation
                        'num_points': 1000,
                        'custom': False
                    }
                plot_sources.append({'type': 'equation'})
                equation_time_specs.append(eqp := eq_params)
                # Assign label
                default_label = f"Theoretical V_o(t) {i + 1}"
                assign_label = get_yes_no("Do you want to assign a custom name for the legend of this graph? [y/n]: ")
                if assign_label == 'y':
                    custom_label = input("Enter legend name: ").strip()
                else:
                    custom_label = default_label
                plot_sources[-1]['label'] = custom_label

        # If multiple graphs are requested, ask if combined plot
        combined_plot = False
        if num_graphs > 1:
            combine_choice = get_yes_no("\nDo you want to combine multiple graphs into one plot? [y/n]: ")
            if combine_choice == 'y':
                combined_plot = True

        # Before asking for new ranges, check if we have saved ranges
        current_x_min, current_x_max = saved_x_min, saved_x_max
        current_y_min, current_y_max = saved_y_min, saved_y_max

        # If we have saved settings, ask if user wants to use them
        if (saved_x_min is not None or saved_x_max is not None or
                saved_y_min is not None or saved_y_max is not None):
            use_saved = get_yes_no("\nDo you want to use previously saved x/y axis ranges? [y/n]: ")
            if use_saved == 'y':
                # Use the saved settings
                x_min, x_max = saved_x_min, saved_x_max
                y_min, y_max = saved_y_min, saved_y_max
            else:
                # Ask new ranges as usual
                specify_yrange = get_yes_no("Do you want to specify vertical (V_o(t)) axis range? [y/n]: ")
                if specify_yrange == 'y':
                    while True:
                        try:
                            y_min = float(input("Enter minimum y-axis value: "))
                            y_max = float(input("Enter maximum y-axis value: "))
                            if y_max <= y_min:
                                print("Maximum y-axis value must be greater than minimum y-axis value.")
                                continue
                            break
                        except ValueError:
                            print("Invalid input. Please enter numerical values for y-axis range.")
                else:
                    y_min = None
                    y_max = None

                specify_xrange = get_yes_no("Do you want to specify horizontal (time) axis range? [y/n]: ")
                if specify_xrange == 'y':
                    while True:
                        try:
                            x_min = float(input("Enter minimum x-axis value (s): "))
                            x_max = float(input("Enter maximum x-axis value (s): "))
                            if x_max <= x_min:
                                print("Maximum x-axis value must be greater than minimum x-axis value.")
                                continue
                            break
                        except ValueError:
                            print("Invalid input. Please enter numerical values for x-axis range.")
                else:
                    x_min = None
                    x_max = None

        else:
            # No saved settings, proceed as usual
            specify_yrange = get_yes_no("\nDo you want to specify vertical (V_o(t)) axis range? [y/n]: ")
            if specify_yrange == 'y':
                while True:
                    try:
                        y_min = float(input("Enter minimum y-axis value: "))
                        y_max = float(input("Enter maximum y-axis value: "))
                        if y_max <= y_min:
                            print("Maximum y-axis value must be greater than minimum y-axis value.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter numerical values for y-axis range.")
            else:
                y_min = None
                y_max = None

            specify_xrange = get_yes_no("Do you want to specify horizontal (time) axis range? [y/n]: ")
            if specify_xrange == 'y':
                while True:
                    try:
                        x_min = float(input("Enter minimum x-axis value (s): "))
                        x_max = float(input("Enter maximum x-axis value (s): "))
                        if x_max <= x_min:
                            print("Maximum x-axis value must be greater than minimum x-axis value.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter numerical values for x-axis range.")
            else:
                x_min = None
                x_max = None

        # After setting ranges, ask if user wants to save these settings
        if (x_min is not None or x_max is not None or y_min is not None or y_max is not None):
            save_settings = get_yes_no("\nDo you want to save these x/y axis settings for future plotting? [y/n]: ")
            if save_settings == 'y':
                saved_x_min, saved_x_max = x_min, x_max
                saved_y_min, saved_y_max = y_min, y_max
            else:
                # Do not change saved settings
                pass
        else:
            # If no range set, no prompt needed to save
            pass

        # Step 2: Determine time range from text files if any
        if any_text_file_used:
            max_time = 0.0
            max_time_data_idx = None
            for ps in plot_sources:
                if ps['type'] == 'text':
                    data_idx = ps['data_index']
                    times = loaded_data_list[data_idx]['times']
                    curr_max = times.max()
                    if curr_max > max_time:
                        max_time = curr_max
                        max_time_data_idx = data_idx

            if max_time_data_idx is not None:
                text_times = loaded_data_list[max_time_data_idx]['times']
                text_min_time = text_times.min()
                text_num_points = len(text_times)
            else:
                text_num_points = 1000
                text_min_time = 0.0
        else:
            max_time = 0.0
            text_num_points = None
            text_min_time = 0.0
            for ps, eqp in zip(plot_sources, equation_time_specs):
                if ps['type'] == 'equation':
                    if eqp and eqp['t_max_user'] > max_time:
                        max_time = eqp['t_max_user']
            if max_time == 0.0:
                max_time = 5e-3  # default max time based on equation

        # Step 3: Update equation parameters if they are not custom and text file used
        if any_text_file_used:
            for eqp in equation_time_specs:
                if eqp is not None and not eqp['custom']:
                    eqp['t_min'] = text_min_time
                    eqp['t_max_user'] = max_time
                    eqp['num_points'] = text_num_points
                    print(
                        "\n[INFO] Since you did not specify parameters for the theoretical convolution output and text file data is present,")
                    print("the following parameters have been adjusted to match the text file data:")
                    print(f"  Minimum Time: {eqp['t_min']} s")
                    print(f"  Maximum Time: {eqp['t_max_user']} s")
                    print(f"  Number of Points: {eqp['num_points']}\n")

        # Prepare plotting
        if combined_plot:
            plt.figure(figsize=(10, 6))

        # Step 4: Plot each graph
        for i, (ps, eqp) in enumerate(zip(plot_sources, equation_time_specs)):
            if ps['type'] == 'equation':
                t_min = eqp['t_min']
                final_max_time = eqp['t_max_user']
                final_num_points = eqp['num_points']

                t = np.linspace(t_min, final_max_time, final_num_points)
                V_o = V_o_theoretical(t)

                label_str = ps.get('label', f"Theoretical V_o(t) {i + 1}")

                if combined_plot:
                    plt.plot(t, V_o, label=label_str, linewidth=2.5, linestyle='--')  # **Thicker and Dashed Line**
                else:
                    plt.figure(figsize=(10, 6))
                    plt.plot(t, V_o, label=label_str, linewidth=2.5, linestyle='--')  # **Thicker and Dashed Line**
                    # Apply x and y limits if specified
                    if x_min is not None and x_max is not None:
                        plt.xlim([x_min, x_max])
                    if y_min is not None and y_max is not None:
                        plt.ylim([y_min, y_max])
                    plt.xlabel("Time (s)")
                    plt.ylabel("Vₒ(t) [V]")
                    plt.title("Theoretical Convolution Output: Vₒ(t)")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

            elif ps['type'] == 'text':
                data_idx = ps['data_index']
                times = loaded_data_list[data_idx]['times']
                V_o = loaded_data_list[data_idx]['V_o']

                label_str = ps.get('label', loaded_data_list[data_idx]['filename'])

                if combined_plot:
                    plt.plot(times, V_o, label=label_str)
                else:
                    plt.figure(figsize=(10, 6))
                    plt.plot(times, V_o, label=label_str)
                    # Apply x and y limits if specified
                    if x_min is not None and x_max is not None:
                        plt.xlim([x_min, x_max])
                    if y_min is not None and y_max is not None:
                        plt.ylim([y_min, y_max])
                    plt.xlabel("Time (s)")
                    plt.ylabel("Vₒ(t) [V]")
                    plt.title("Convolution Output from Simulation Data")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

        if combined_plot:
            # **Apply styles only to theoretical graphs**
            # Since plt.plot was called earlier with styles for theoretical graphs,
            # and default styles for text graphs, no additional styling is needed here.

            if x_min is not None and x_max is not None:
                plt.xlim([x_min, x_max])
            if y_min is not None and y_max is not None:
                plt.ylim([y_min, y_max])
            plt.xlabel("Time (s)")
            plt.ylabel("Vₒ(t) [V]")
            plt.title("Combined Convolution Output Plots")
            plt.grid(True, which="both", ls="--")
            plt.legend()
            plt.show()

        # After plotting, ask user if they want to continue
        cont_choice = get_yes_no("\nDo you want to plot again? [y/n]: ")
        if cont_choice != 'y':
            print("Exiting the plotting tool. Goodbye!")
            break


if __name__ == "__main__":
    main()
