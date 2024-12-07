import numpy as np
import matplotlib.pyplot as plt

# Given parameters
R = 100.0  # ohms, example value
L = 1e-3   # henries, example value
tau = L/R

# Time discretization
dt = 1e-6            # time step: 1 microsecond
t_max = 3e-3          # simulate up to 3 ms
t = np.arange(0, t_max, dt)

# Define S(t):
# S(t) = 0; t<0
#      = 0.5; 0<t<1ms
#      = 1;   1ms<t<2ms
#      = 0;   t>2ms
S = np.zeros_like(t)
S[(t > 0) & (t < 1e-3)] = 0.5
S[(t >= 1e-3) & (t < 2e-3)] = 1.0
# after 2 ms, S=0, so no update needed

# Define H(t):
# H(t) = δ(t) - (R/L)*exp(-R/L t)u(t)
# For t < 0, H(t)=0 (causality)
H = np.zeros_like(t)
# Approximate delta at t=0:
H[0] = 1.0/dt  # delta approximation

# For t>0, H(t) = - (R/L)*exp(-R/L t)
H[t > 0] = H[t > 0] - (R/L)*np.exp(-(R/L)*t[t > 0])

# Convolution using numpy.
# Note: np.convolve gives result length = len(S)+len(H)-1
Vo_full = np.convolve(S, H, mode='full')*dt
# The multiplication by dt is crucial because we represented delta as 1/dt.
# Convolution in discrete-time is sum S[k]*H[n-k]. Since we used delta = 1/dt,
# integrating with dt is needed to get correct continuous-time scaling.

# Time axis for Vo after convolution
t_Vo = np.arange(0, len(Vo_full)*dt, dt)

# We only need up to t_max (or a bit beyond to see the full response)
# Trim if needed
max_index = np.where(t_Vo >= t_max)[0][0]
t_Vo = t_Vo[:max_index]
Vo = Vo_full[:max_index]

# Plot the results
plt.figure(figsize=(10,6))

# Plot input
plt.subplot(2,1,1)
plt.plot(t*1e3, S, label='S(t)')
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title('Input Signal S(t)')
plt.grid(True)
plt.legend()

# Plot output
plt.subplot(2,1,2)
plt.plot(t_Vo*1e3, Vo, label='Vo(t)', color='red')
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title('Output Response Vo(t) = S(t)*H(t)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
