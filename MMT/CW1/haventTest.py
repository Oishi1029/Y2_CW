import numpy as np
import matplotlib.pyplot as plt

def load_text_file_data(filename):
    """
    Load text file data of format:
    Freq    (Mag_dB,Phase_deg)
    Example line:
    1.00000000000000e-01  (-7.35764055785593e+01dB,-4.25229053769058e-02∞)
    
    We'll parse lines ignoring the '∞' symbol which is shown as degrees symbol. 
    We assume the phase is shown as something∞ and we remove that.
    """
    freqs = []
    mags_dB = []
    phases_deg = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Freq"):
                continue
            parts = line.split()
            # parts[0] = frequency, parts[1] = (Mag_dB,Phase_deg∞)
            freq = float(parts[0])
            # Now parse the magnitude and phase from the second part
            # Format: (-7.65867050261857e+01dB,0.00000000000000e+00∞)
            data_str = parts[1]
            
            # Remove parentheses
            data_str = data_str.strip("()")
            # Now split by comma
            mag_str, phase_str = data_str.split(',')
            
            # Remove 'dB' from mag_str
            mag_str = mag_str.replace('dB','')
            # Remove '∞' or degree symbol from phase_str
            phase_str = phase_str.replace('∞','')
            
            mag_dB = float(mag_str)
            phase_deg = float(phase_str)
            
            freqs.append(freq)
            mags_dB.append(mag_dB)
            phases_deg.append(phase_deg)
            
    return np.array(freqs), np.array(mags_dB), np.array(phases_deg)


def S2_equation(omega, m=1.0):
    # S_2(ω) = [(sin(2mω)-0.5*sin(mω))/ω] + j[(cos(2mω)-0.5*cos(mω)-0.5)/ω]
    # Be careful with ω=0, we can handle limit as ω->0 if needed, or start from a small positive freq.
    # For plotting, we usually start from a minimum freq > 0.
    # If ω=0 occurs, we can set S2=0 or handle limit properly. Here we just avoid ω=0 by adding a small epsilon.
    epsilon = 1e-15
    denom = np.where(omega==0, epsilon, omega)
    real_part = (np.sin(2*m*omega) - 0.5*np.sin(m*omega)) / denom
    imag_part = (np.cos(2*m*omega) - 0.5*np.cos(m*omega) - 0.5) / denom
    return real_part + 1j*imag_part


def convert_dB_to_linear(dB_val):
    # Convert magnitude in dB to linear scale
    return 10**(dB_val/20.0)


def main():
    # Store loaded text file data in a list for reuse.
    # Each entry: {'filename':..., 'freqs':..., 'mags_dB':..., 'phases_deg':...}
    loaded_data_list = []
    
    while True:
        # Ask user how many graphs to plot
        num_graphs = int(input("How many graphs do you want to plot? "))
        
        # For each graph, ask if from text file or equation
        plot_sources = []  # list of dicts: {'type': 'text' or 'equation', 'data_index': ... or 'filename': ...}
        any_text_file_used = False
        
        for i in range(num_graphs):
            print(f"For graph {i+1}:")
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
                        continue
                # If not reusing:
                filename = input("Enter the text file name/path: ").strip()
                freqs, mags_dB, phases_deg = load_text_file_data(filename)
                loaded_data_list.append({'filename': filename, 'freqs': freqs, 'mags_dB': mags_dB, 'phases_deg': phases_deg})
                plot_sources.append({'type': 'text', 'data_index': len(loaded_data_list)-1})
            else:
                # Equation based
                plot_sources.append({'type': 'equation'})
        
        # Ask if multiple graph in one plot if num_graphs > 1
        combined_plot = False
        if num_graphs > 1:
            combine_choice = input("Do you want to combine multiple graphs into one plot? [y/n]: ").strip().lower()
            if combine_choice == 'y':
                combined_plot = True
        
        # Ask user for linear scale or dB scale
        scale_choice = input("Do you want linear scale or dB scale? [linear/dB]: ").strip().lower()
        linear_scale = (scale_choice == 'linear')
        
        # Determine maximum frequency range:
        # If any text file used, max freq = max freq found in text files used in this round
        if any_text_file_used:
            max_freq = 0.0
            for ps in plot_sources:
                if ps['type'] == 'text':
                    data_idx = ps['data_index']
                    freqs = loaded_data_list[data_idx]['freqs']
                    if freqs.max() > max_freq:
                        max_freq = freqs.max()
        else:
            # Default max freq: 10kHz
            max_freq = 1e4
        
        # Prepare plotting
        if combined_plot:
            plt.figure(figsize=(10,6))
        
        for i, ps in enumerate(plot_sources):
            if ps['type'] == 'equation':
                # Generate frequency vector from 0 to max_freq
                # Avoid 0 exactly to prevent divide by zero
                freqs = np.linspace(1e-3, max_freq, 1000)  
                # Angular frequency ω = 2πf
                omega = 2 * np.pi * freqs
                S2 = S2_equation(omega)
                mag_lin = np.abs(S2)
                if linear_scale:
                    # just plot linear magnitude
                    ydata = mag_lin
                else:
                    # plot in dB scale
                    ydata = 20 * np.log10(mag_lin + 1e-30)  # +1e-30 to avoid log(0)
                
                # Plot
                if combined_plot:
                    plt.plot(freqs, ydata, label=f"Equation {i+1}")
                else:
                    plt.figure(figsize=(10,6))
                    plt.plot(freqs, ydata, label="Equation")
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("FFT from Equation")
                    plt.grid(True)
                    plt.legend()
                    plt.show()
                    
            else:
                # From text file data
                data_idx = ps['data_index']
                freqs = loaded_data_list[data_idx]['freqs']
                mags_dB = loaded_data_list[data_idx]['mags_dB']
                # If linear scale chosen, convert dB to linear
                if linear_scale:
                    ydata = convert_dB_to_linear(mags_dB)
                else:
                    ydata = mags_dB
                
                if combined_plot:
                    plt.plot(freqs, ydata, label=loaded_data_list[data_idx]['filename'])
                else:
                    plt.figure(figsize=(10,6))
                    plt.plot(freqs, ydata, label=loaded_data_list[data_idx]['filename'])
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
                    plt.title("FFT from Text File Data")
                    plt.grid(True)
                    plt.legend()
                    plt.show()
        
        if combined_plot:
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude" + (" (linear)" if linear_scale else " (dB)"))
            plt.title("Combined FFT Plots")
            plt.grid(True)
            plt.legend()
            plt.show()
        
        # After plotting, ask user if they want to continue
        cont_choice = input("Do you want to plot again? [y/n]: ").strip().lower()
        if cont_choice != 'y':
            break

if __name__ == "__main__":
    main()
