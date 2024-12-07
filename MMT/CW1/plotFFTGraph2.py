import numpy as np
import matplotlib.pyplot as plt


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
            # Remove degree symbol '°'
            phase_str = phase_str.replace('°', '')
            # If there's any other symbol like '∞', remove it as well
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
    # Store loaded text file data in a list for reuse.
    loaded_data_list = []

    while True:
        num_graphs = int(input("How many graphs do you want to plot? "))

        plot_sources = []  # list of dicts: {'type': 'text' or 'equation', 'data_index': ... , 'freq_params': {...}}
        any_text_file_used = False

        equation_freq_specs = []

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
                        'num_points': num_points
                    }
                else:
                    # Default if no specification and no text used
                    eq_params = {
                        'min_freq': 1e-3,  # start at a small positive frequency to avoid log(0)
                        'max_freq_user': 1e4,
                        'num_points': 1000
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

        # Determine maximum frequency range:
        if any_text_file_used:
            # Max frequency from text files used in this round
            max_freq = 0.0
            for ps in plot_sources:
                if ps['type'] == 'text':
                    data_idx = ps['data_index']
                    freqs = loaded_data_list[data_idx]['freqs']
                    if freqs.max() > max_freq:
                        max_freq = freqs.max()
        else:
            # No text file used, use eq parameters
            max_freq = 0.0
            for ps, eqp in zip(plot_sources, equation_freq_specs):
                if ps['type'] == 'equation':
                    if eqp['max_freq_user'] > max_freq:
                        max_freq = eqp['max_freq_user']
            if max_freq == 0.0:
                max_freq = 1e4

        # Prepare plotting
        if combined_plot:
            plt.figure(figsize=(10, 6))

        # Plot each graph
        for i, (ps, eqp) in enumerate(zip(plot_sources, equation_freq_specs)):
            if ps['type'] == 'equation':
                if any_text_file_used:
                    # Override max_freq with that from text file
                    min_freq = eqp['min_freq'] if eqp is not None else 1e-3
                    num_points = eqp['num_points'] if eqp is not None else 1000
                    freqs = np.linspace(min_freq, max_freq, num_points)
                else:
                    # no text used, just use eqp parameters directly
                    min_freq = eqp['min_freq']
                    num_points = eqp['num_points']
                    freqs = np.linspace(min_freq, max_freq, num_points)

                omega = 2 * np.pi * freqs
                S2 = S2_equation(omega)
                mag_lin = np.abs(S2)
                if linear_scale:
                    ydata = mag_lin
                else:
                    ydata = 20 * np.log10(mag_lin + 1e-30)

                label_str = f"Equation {i + 1}"
                if combined_plot:
                    plt.plot(freqs, ydata, label=label_str)
                else:
                    plt.figure(figsize=(10, 6))
                    if use_log_scale:
                        plt.xscale('log')
                    plt.plot(freqs, ydata, label=label_str)
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("FFT from Equation")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

            else:
                # Text file data
                data_idx = ps['data_index']
                freqs = loaded_data_list[data_idx]['freqs']
                mags_dB = loaded_data_list[data_idx]['mags_dB']
                if linear_scale:
                    ydata = convert_dB_to_linear(mags_dB)
                else:
                    ydata = mags_dB

                label_str = loaded_data_list[data_idx]['filename']
                if combined_plot:
                    plt.plot(freqs, ydata, label=label_str)
                else:
                    plt.figure(figsize=(10, 6))
                    if use_log_scale:
                        plt.xscale('log')
                    plt.plot(freqs, ydata, label=label_str)
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("FFT from Text File Data")
                    plt.grid(True, which="both", ls="--")
                    plt.legend()
                    plt.show()

        if combined_plot:
            if use_log_scale:
                plt.xscale('log')
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
            plt.title("Combined FFT Plots")
            plt.grid(True, which="both", ls="--")
            plt.legend()
            plt.show()

        # After plotting, ask user if they want to continue
        cont_choice = input("Do you want to plot again? [y/n]: ").strip().lower()
        if cont_choice != 'y':
            break


if __name__ == "__main__":
    main()
