import numpy as np
import matplotlib.pyplot as plt

# Global saved settings
saved_x_min = None
saved_x_max = None
saved_y_min = None
saved_y_max = None

def load_text_file_data(filename):
    freqs = []
    mags_dB = []
    phases_deg = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Freq"):
                continue
            parts = line.split()
            freq = float(parts[0])
            data_str = parts[1].strip("()")

            mag_str, phase_str = data_str.split(',')

            # Remove 'dB'
            mag_str = mag_str.replace('dB', '')
            # Remove degree symbol '°' and '∞' if present
            phase_str = phase_str.replace('°', '')
            phase_str = phase_str.replace('∞', '')

            mag_dB = float(mag_str)
            phase_deg = float(phase_str)

            freqs.append(freq)
            mags_dB.append(mag_dB)
            phases_deg.append(phase_deg)

    return np.array(freqs), np.array(mags_dB), np.array(phases_deg)


def S2_equation(omega, m=0.001):
    epsilon = 1e-15
    denom = np.where(omega == 0, epsilon, omega)
    real_part = (np.sin(2 * m * omega) - 0.5 * np.sin(m * omega)) / denom
    imag_part = (np.cos(2 * m * omega) - 0.5 * np.cos(m * omega) - 0.5) / denom
    return real_part + 1j * imag_part


def convert_dB_to_linear(dB_val):
    return 10 ** (dB_val / 20.0)


def main():
    global saved_x_min, saved_x_max, saved_y_min, saved_y_max

    # Store loaded text file data in a list for reuse.
    loaded_data_list = []

    while True:
        num_graphs = int(input("How many graphs do you want to plot? "))

        plot_sources = []
        equation_freq_specs = []
        any_text_file_used = False

        # Step 1: Gather user input for each graph
        for i in range(num_graphs):
            print(f"For graph {i + 1}:")
            source_type = input("Is this graph from text file (t) or equation (e)? [t/e]: ").strip().lower()
            if source_type == 't':
                any_text_file_used = True
                # If text file data used before, prompt if user wants to reuse existing data
                if len(loaded_data_list) > 0:
                    print("You have previously loaded text file data:")
                    for idx, d in enumerate(loaded_data_list):
                        print(f"{idx}: {d['filename']}")
                    reuse_choice = input("Do you want to reuse previously loaded data? [y/n]: ").strip().lower()
                    if reuse_choice == 'y':
                        chosen_idx = int(input("Enter the index of the previously loaded data to use: "))
                        plot_sources.append({'type': 'text', 'data_index': chosen_idx})
                        equation_freq_specs.append(None)
                        continue
                # If not reusing:
                filename = input("Enter the text file name/path: ").strip()
                freqs, mags_dB, phases_deg = load_text_file_data(filename)
                loaded_data_list.append(
                    {'filename': filename, 'freqs': freqs, 'mags_dB': mags_dB, 'phases_deg': phases_deg})
                plot_sources.append({'type': 'text', 'data_index': len(loaded_data_list) - 1})
                equation_freq_specs.append(None)
            else:
                # Equation based
                custom_choice = input(
                    "Do you want to specify frequency range and sample points for the equation? [y/n]: ").strip().lower()
                if custom_choice == 'y':
                    min_freq = float(input("Enter minimum frequency (Hz): "))
                    max_freq_user = float(input("Enter maximum frequency (Hz): "))
                    num_points = int(input("Enter number of sample points: "))
                    eq_params = {
                        'min_freq': min_freq,
                        'max_freq_user': max_freq_user,
                        'num_points': num_points,
                        'custom': True
                    }
                else:
                    eq_params = {
                        'min_freq': 1e-3,
                        'max_freq_user': 1e4,
                        'num_points': 1000,
                        'custom': False
                    }
                plot_sources.append({'type': 'equation'})
                equation_freq_specs.append(eq_params)

        # If multiple graphs are requested, ask if combined plot
        combined_plot = False
        if num_graphs > 1:
            combine_choice = input("Do you want to combine multiple graphs into one plot? [y/n]: ").strip().lower()
            if combine_choice == 'y':
                combined_plot = True

        # Ask user for linear scale or dB scale
        scale_choice = input("Do you want linear scale or dB scale? [linear/dB]: ").strip().lower()
        linear_scale = (scale_choice == 'linear')

        # Ask user if they want a logarithmic frequency axis
        log_choice = input("Do you want the frequency axis to be logarithmic? [y/n]: ").strip().lower()
        use_log_scale = (log_choice == 'y')

        # Before asking for new ranges, check if we have saved ranges
        current_x_min, current_x_max = saved_x_min, saved_x_max
        current_y_min, current_y_max = saved_y_min, saved_y_max

        # If we have saved settings, ask if user wants to use them
        if (saved_x_min is not None or saved_x_max is not None or
            saved_y_min is not None or saved_y_max is not None):
            use_saved = input("Do you want to use previously saved x/y axis ranges? [y/n]: ").strip().lower()
            if use_saved == 'y':
                # Use the saved settings
                x_min, x_max = saved_x_min, saved_x_max
                y_min, y_max = saved_y_min, saved_y_max
            else:
                # Ask new ranges as usual
                specify_yrange = input("Do you want to specify vertical axis range? [y/n]: ").strip().lower()
                if specify_yrange == 'y':
                    y_min = float(input("Enter minimum y-axis value: "))
                    y_max = float(input("Enter maximum y-axis value: "))
                else:
                    y_min = None
                    y_max = None

                specify_xrange = input("Do you want to specify horizontal (frequency) axis range? [y/n]: ").strip().lower()
                if specify_xrange == 'y':
                    x_min = float(input("Enter minimum x-axis value (Hz): "))
                    x_max = float(input("Enter maximum x-axis value (Hz): "))
                else:
                    x_min = None
                    x_max = None

        else:
            # No saved settings, proceed as usual
            specify_yrange = input("Do you want to specify vertical axis range? [y/n]: ").strip().lower()
            if specify_yrange == 'y':
                y_min = float(input("Enter minimum y-axis value: "))
                y_max = float(input("Enter maximum y-axis value: "))
            else:
                y_min = None
                y_max = None

            specify_xrange = input("Do you want to specify horizontal (frequency) axis range? [y/n]: ").strip().lower()
            if specify_xrange == 'y':
                x_min = float(input("Enter minimum x-axis value (Hz): "))
                x_max = float(input("Enter maximum x-axis value (Hz): "))
            else:
                x_min = None
                x_max = None

        # After setting ranges, ask if user wants to save these settings
        if (x_min is not None or x_max is not None or y_min is not None or y_max is not None):
            save_settings = input("Do you want to save these x/y axis settings for future plotting? [y/n]: ").strip().lower()
            if save_settings == 'y':
                saved_x_min, saved_x_max = x_min, x_max
                saved_y_min, saved_y_max = y_min, y_max
            else:
                # Do not change saved settings
                pass
        else:
            # If no range set, no prompt needed to save
            pass

        # Step 2: Determine frequency range from text files if any
        if any_text_file_used:
            max_freq = 0.0
            max_freq_data_idx = None
            for ps in plot_sources:
                if ps['type'] == 'text':
                    data_idx = ps['data_index']
                    freqs = loaded_data_list[data_idx]['freqs']
                    curr_max = freqs.max()
                    if curr_max > max_freq:
                        max_freq = curr_max
                        max_freq_data_idx = data_idx

            if max_freq_data_idx is not None:
                text_freqs = loaded_data_list[max_freq_data_idx]['freqs']
                text_min_freq = text_freqs.min()
                text_num_points = len(text_freqs)
            else:
                text_num_points = 1000
                text_min_freq = 1e-3
        else:
            max_freq = 0.0
            text_num_points = None
            text_min_freq = 1e-3
            for ps, eqp in zip(plot_sources, equation_freq_specs):
                if ps['type'] == 'equation':
                    if eqp and eqp['max_freq_user'] > max_freq:
                        max_freq = eqp['max_freq_user']
            if max_freq == 0.0:
                max_freq = 1e4

        # Step 3: Update equation parameters if they are not custom and text file used
        if any_text_file_used:
            for eqp in equation_freq_specs:
                if eqp is not None and not eqp['custom']:
                    eqp['min_freq'] = text_min_freq
                    eqp['max_freq_user'] = max_freq
                    eqp['num_points'] = text_num_points
                    print("\n[INFO] Since you did not specify parameters for the equation-based FFT and text file FFT data is present,")
                    print("the following parameters have been adjusted to match the text file FFT graph:")
                    print(f"  Minimum Frequency: {eqp['min_freq']} Hz")
                    print(f"  Maximum Frequency: {eqp['max_freq_user']} Hz")
                    print(f"  Number of Points: {eqp['num_points']}\n")

        # Prepare plotting
        if combined_plot:
            plt.figure(figsize=(10, 6))

        # Step 4: Plot each graph
        for i, (ps, eqp) in enumerate(zip(plot_sources, equation_freq_specs)):
            if ps['type'] == 'equation':
                min_freq = eqp['min_freq']
                final_max_freq = eqp['max_freq_user']
                final_num_points = eqp['num_points']

                freqs = np.linspace(min_freq, final_max_freq, final_num_points)
                omega = 2 * np.pi * freqs

                S2 = S2_equation(omega)
                mag_lin = np.abs(S2)

                max_amp = mag_lin.max()
                mag_lin_normalized = mag_lin / max_amp

                if linear_scale:
                    ydata = mag_lin_normalized
                else:
                    ydata = 20 * np.log10(mag_lin_normalized + 1e-30)

                label_str = f"Equation {i + 1}"
                if combined_plot:
                    plt.plot(freqs, ydata, label=label_str)
                else:
                    plt.figure(figsize=(10, 6))
                    if use_log_scale:
                        plt.xscale('log')
                    plt.plot(freqs, ydata, label=label_str)
                    # Apply x and y limits if specified
                    if x_min is not None and x_max is not None:
                        plt.xlim([x_min, x_max])
                    if y_min is not None and y_max is not None:
                        plt.ylim([y_min, y_max])
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Normalized Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("Normalized FFT from Equation")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

            elif ps['type'] == 'text':
                data_idx = ps['data_index']
                freqs = loaded_data_list[data_idx]['freqs']
                mags_dB = loaded_data_list[data_idx]['mags_dB']

                mags_lin = convert_dB_to_linear(mags_dB)
                max_amp = mags_lin.max()
                mags_lin_normalized = mags_lin / max_amp

                if linear_scale:
                    ydata = mags_lin_normalized
                else:
                    ydata = 20 * np.log10(mags_lin_normalized + 1e-30)

                label_str = loaded_data_list[data_idx]['filename']
                if combined_plot:
                    plt.plot(freqs, ydata, label=label_str)
                else:
                    plt.figure(figsize=(10, 6))
                    if use_log_scale:
                        plt.xscale('log')
                    plt.plot(freqs, ydata, label=label_str)
                    # Apply x and y limits if specified
                    if x_min is not None and x_max is not None:
                        plt.xlim([x_min, x_max])
                    if y_min is not None and y_max is not None:
                        plt.ylim([y_min, y_max])
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Normalized Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("Normalized FFT from Text File Data")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

        if combined_plot:
            if use_log_scale:
                plt.xscale('log')
            if x_min is not None and x_max is not None:
                plt.xlim([x_min, x_max])
            if y_min is not None and y_max is not None:
                plt.ylim([y_min, y_max])
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Normalized Magnitude" + (" (linear)" if linear_scale else " (dB)"))
            plt.title("Combined Normalized FFT Plots")
            plt.grid(True, which="both", ls="--")
            plt.legend()
            plt.show()

        # After plotting, ask user if they want to continue
        cont_choice = input("Do you want to plot again? [y/n]: ").strip().lower()
        if cont_choice != 'y':
            break


if __name__ == "__main__":
    main()
