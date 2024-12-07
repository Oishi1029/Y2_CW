import numpy as np
import matplotlib.pyplot as plt

# Parameters
R = 100.0  # Ohms
L = 1e-3  # Henry
tau = L / R  # Time constant
dt = 1e-6  # Time step: 1 microsecond
t_end = 3e-3  # End simulation at 3 ms

t = np.arange(0, t_end, dt)


# Define S(t) piecewise
def S(t):
    # 0 for t<0 or t>=2ms
    # 0.5 for 0<=t<1ms
    # 1 for 1ms<=t<2ms
    if t < 0:
        return 0.0
    elif t < 1e-3:
        return 0.5
    elif t < 2e-3:
        return 1.0
    else:
        return 0.0


# Vectorize S for efficiency
S_vec = np.vectorize(S)

S_values = S_vec(t)

# Define Vo(t) based on integral
# Vo(t) = S(t) - (R/L)*Integral_0^{min(t,2ms)} S(tau)*exp(-(R/L)*(t-tau)) d tau

Vo = np.zeros_like(t)

for i, ti in enumerate(t):
    # First get the delta part: S(ti)
    part_delta = S(ti)

    # Determine integration limits
    upper_limit = min(ti, 2e-3)

    if upper_limit <= 0:
        # no integral contribution if t<0
        integral_part = 0
    else:
        # We integrate from tau=0 to tau=upper_limit
        # We'll do numeric integration:
        tau_values = np.arange(0, upper_limit, dt)
        integrand = S_vec(tau_values) * np.exp(-(R / L) * (ti - tau_values))
        integral_part = np.trapz(integrand, tau_values)  # numerical integration using trapezoidal rule

    Vo[i] = part_delta - (R / L) * integral_part

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t * 1e3, Vo, label='Vo(t)')
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title('Output Vo(t) = (S*H)(t)')
plt.grid(True)
plt.legend()

# Also plot S(t) to visualize the input
plt.figure(figsize=(10, 3))
plt.plot(t * 1e3, S_values, label='S(t)', color='orange')
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title('Input S(t)')
plt.grid(True)
plt.legend()

plt.show()
