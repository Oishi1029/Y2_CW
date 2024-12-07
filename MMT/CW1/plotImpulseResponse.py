import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 1  # Resistance in ohms
L = 1  # Inductance in henries
t = np.linspace(0, 5, 1000)  # Time range

# Impulse response function
H = np.where(t == 0, 1, 0) - (R / L) * np.exp(-R / L * t)

# Plot the impulse response
plt.figure(figsize=(10, 6))
plt.plot(t, H, label=r"$H(t) = \delta(t) - \frac{R}{L} e^{-\frac{R}{L} t}$")
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.title("Impulse Response")
plt.xlabel("Time (t)")
plt.ylabel("H(t)")
plt.legend()
plt.grid(True)
plt.show()
