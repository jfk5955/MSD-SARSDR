import numpy as np
from scipy.io import savemat

# Dimensions
rows, cols = 80, 300

# Generate random complex numbers
real_part = np.random.randn(rows, cols)
imag_part = np.random.randn(rows, cols)
complex_matrix = real_part + 1j * imag_part

# Package into a dictionary
mdic = {"complex_data": complex_matrix}

# Save to a .mat file
savemat("complex_matrix.mat", mdic)

print("Matrix saved to 'complex_matrix.mat'")
