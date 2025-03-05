import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

def main():
    
    # Parameters
    V_ref = 4.0    # Reference voltage (0-4V)
    n_bits = 2     # ADC resolution (2 bits = 4 steps)
    step = 0.0001  # Voltage step for analysis

    # Generate voltages from 0V to V_ref
    V_in = np.arange(0, V_ref + step, step)

    # Correct code assignment for an n-bit ADC
    max_code = (2**n_bits) - 1  # = 3 for 2-bit ADC
    codes = np.floor(V_in * (2**n_bits) / V_ref).astype(int)
    codes = np.clip(codes, 0, max_code)  # Clamp codes to valid range

    # Conversion methods - reordered according to request
    def method1(code):
        return code * (V_ref / max_code)     # Divide by 3 (incorrect method)

    def method2(code):
        return code * (V_ref / (2**n_bits))  # Divide by 4 (correct approach)

    def method3(code):
        return (code + 0.5) * (V_ref / (2**n_bits))  # Add 0.5 LSB (optimal approach)

    # Calculate voltages and errors
    V_method1 = method1(codes)
    V_method2 = method2(codes)
    V_method3 = method3(codes)

    error_method1 = np.abs(V_in - V_method1)
    error_method2 = np.abs(V_in - V_method2)
    error_method3 = np.abs(V_in - V_method3)

    # Plotting with interactive controls
    fig = plt.figure(figsize=(14, 10))

    # Plot 1: Voltage Conversion
    ax1 = plt.subplot(2, 1, 1)
    ideal_line, = plt.plot(V_in, V_in, 'k--', label='Ideal ADC', alpha=0.7)
    method1_line, = plt.plot(V_in, V_method1, 'r', label=f'Method 1 (Divide by {max_code})')
    method2_line, = plt.plot(V_in, V_method2, 'g', label=f'Method 2 (Divide by {2**n_bits})')
    method3_line, = plt.plot(V_in, V_method3, 'b', label='Method 3 (Divide by 4 + 0.5 LSB)')

    plt.xlabel('Input Voltage (V)')
    plt.ylabel('Calculated Voltage (V)')
    plt.title(f'{n_bits}-bit ADC Voltage Conversion (V_ref = {V_ref}V)')
    plt.grid(True)
    plt.legend()

    # Plot 2: Error Analysis
    ax2 = plt.subplot(2, 1, 2)
    error1_line, = plt.plot(V_in, error_method1, 'r', label='Method 1 Error')
    error2_line, = plt.plot(V_in, error_method2, 'g', label='Method 2 Error')
    error3_line, = plt.plot(V_in, error_method3, 'b', label='Method 3 Error')

    plt.xlabel('Input Voltage (V)')
    plt.ylabel('Absolute Error (V)')
    plt.title(f'Error Analysis (Max Errors: Method 1={np.max(error_method1):.4f}V, Method 2={np.max(error_method2):.4f}V, Method 3={np.max(error_method3):.4f}V)')
    plt.grid(True)
    plt.legend()

    # Add checkboxes to toggle visibility
    plt.subplots_adjust(left=0.1, bottom=0.25)
    checkbox_ax = plt.axes([0.25, 0.05, 0.5, 0.1])

    lines = [ideal_line, method1_line, method2_line, method3_line,
             error1_line, error2_line, error3_line]
    labels = ['Ideal', 'Method 1 (÷3)', 'Method 2 (÷4)', 'Method 3 (÷4 + 0.5 LSB)',
              'Method 1 Error', 'Method 2 Error', 'Method 3 Error']
    visibility = [True] * len(lines)

    check = CheckButtons(checkbox_ax, labels, visibility)

    def toggle_visibility(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        fig.canvas.draw_idle()

    check.on_clicked(toggle_visibility)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Make room for checkboxes
    plt.show()


if __name__ == "__main__":
    main()