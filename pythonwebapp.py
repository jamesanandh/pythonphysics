import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Helper functions
def dms_to_decimal(deg, minutes):
    """Convert degrees and minutes to decimal degrees."""
    return deg + (minutes / 60)

def decimal_to_dms(decimal_degrees):
    """Convert decimal degrees to degrees, minutes, and properly rounded seconds."""
    degrees = int(decimal_degrees)
    minutes_decimal = (decimal_degrees - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = round((minutes_decimal - minutes) * 60)
    if seconds == 60:
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        degrees += 1
    return degrees, minutes, seconds

def calculate_value(theta_deg, theta_min, l):
    """Calculate (θ) / (10 × l) and return result in DMS format."""
    theta_decimal = dms_to_decimal(theta_deg, theta_min)
    result_decimal = theta_decimal / (10 * l)
    return decimal_to_dms(result_decimal)

def calculate_error_percentage(standard_deg, standard_min, observed_deg, observed_min):
    """Calculate error percentage given standard and observed values in degrees and minutes."""
    standard_decimal = dms_to_decimal(standard_deg, standard_min)
    observed_decimal = dms_to_decimal(observed_deg, observed_min)
    error_percentage = abs((standard_decimal - observed_decimal) / standard_decimal) * 100
    return round(error_percentage, 2)

# Program 1: Spectrometer
def program_1():
    st.header("Program 1: Polarimeter")
    theta_deg = st.number_input("Enter θ/c degrees:", value=0)
    theta_min = st.number_input("Enter θ/c minutes:", value=0.0)
    l = st.number_input("Enter l (in meter):", value=1.0)

    if st.button("Calculate Value"):
        result_d, result_m, result_s = calculate_value(theta_deg, theta_min, l)
        st.success(f"Calculated Value: {result_d}° {result_m}' {result_s}\"")

    # Error calculation
    st.subheader("Error Calculation")
    standard_deg = st.number_input("Enter standard value degrees:", value=0)
    standard_min = st.number_input("Enter standard value minutes:", value=0.0)
    observed_deg = st.number_input("Enter observed value degrees:", value=0)
    observed_min = st.number_input("Enter observed value minutes:", value=0.0)

    if st.button("Calculate Error Percentage"):
        error_percent = calculate_error_percentage(standard_deg, standard_min, observed_deg, observed_min)
        st.success(f"Error Percentage: {error_percent}%")

# Program 2: Calibration of a high range voltmeter
def program_2():
    st.header("Program 2: Calibration of a High Range Voltmeter")
    n = st.number_input("Enter the number of calculations:", value=1, min_value=1)
    l1 = st.number_input("Enter l1:", value=1.0)

    V_list = []
    l2_list = []
    V_prime_list = []
    correction_list = []

    for i in range(n):
        st.subheader(f"Calculation {i + 1}")
        V = st.number_input(f"Enter V for calculation {i + 1}:", value=0.0)
        l2 = st.number_input(f"Enter l2 for calculation {i + 1}:", value=0.0)

        V_prime = 50 * 1.08 * l2 / l1
        correction = V_prime - V

        V_list.append(V)
        l2_list.append(l2)
        V_prime_list.append(V_prime)
        correction_list.append(correction)

    if st.button("Generate Results"):
        # Create a list of lists for the table data
        table_data = []
        for i in range(n):
            table_data.append([V_list[i], l2_list[i], V_prime_list[i], correction_list[i]])

        # Define headers
        headers = ["Voltmeter readings", "l2", "V' (Calculated Voltage)", "Correction (V' - V)"]

        # Display the table using st.table
        st.table([headers] + table_data)

        # Plot graphs
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Graph 1: V vs. Correction (V' - V)
        ax1.scatter(V_list, correction_list, color='red', marker='o', label="Correction (V' - V)")
        ax1.plot(V_list, correction_list, linestyle='--', alpha=0.7, color='red')
        ax1.set_xlabel("V")
        ax1.set_ylabel("V' - V (Correction)")
        ax1.set_title("Graph 1: V vs. Correction")
        ax1.legend()
        ax1.grid(True)

        # Graph 2: V vs. V'
        ax2.scatter(V_list, V_prime_list, color='blue', marker='o', label="V'")
        ax2.plot(V_list, V_prime_list, linestyle='--', alpha=0.7, color='blue')
        ax2.set_xlabel("V")
        ax2.set_ylabel("V'")
        ax2.set_title("Graph 2: V vs. V'")
        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig)

# Program 3: Sonometer
def program_3():
    st.header("Program 3: Sonometer")

    def calculate_mass_of_wire(r, rho):
        """Calculate mass per unit length (m) using m = π(r^2)ρ."""
        return math.pi * (r ** 2) * rho

    def calculate_frequency(M, g, r, rho):
        """Calculate the frequency of the tuning fork."""
        mass_of_wire = calculate_mass_of_wire(r, rho)
        frequency = (1 / 2) * math.sqrt((M * g) / mass_of_wire)
        return frequency

    M = st.number_input("Enter the mass/length^2 (M/l²) in kg/m²:", value=0.0)
    g = 9.81  # Acceleration due to gravity in m/s^2
    r = st.number_input("Enter the radius of the wire (r) in meters:", value=0.0)
    rho = st.number_input("Enter the density of the wire (ρ) in kg/m^3:", value=0.0)

    if st.button("Calculate Frequency"):
        frequency = calculate_frequency(M, g, r, rho)
        st.success(f"Frequency of the tuning fork: {frequency:.2f} Hz")

# Program 4: BG absolute capacity of a condenser
def program_4():
    st.header("Program 4: BG Absolute Capacity of a Condenser")

    def calculate_C(T, d1_R2, r2_d2, G, a1, a11):
        lambda_value = round((2.303 / 10) * math.log10(a1 / a11), 4)
        C = (T / (2 * math.pi * G)) * d1_R2 * r2_d2 * (1 + (lambda_value / 2))
        C_microfarad = round(C * 1e6, 4)
        return lambda_value, C_microfarad

    T = st.number_input("Enter T:", value=0.0)
    d1_R2 = st.number_input("Enter d1/R2:", value=0.0)
    r2_d2 = st.number_input("Enter r2/d2:", value=0.0)
    G = st.number_input("Enter G:", value=0.0)
    a1 = st.number_input("Enter a1:", value=0.0)
    a11 = st.number_input("Enter a11:", value=0.0)

    if st.button("Calculate Capacitance"):
        lambda_value, C_value = calculate_C(T, d1_R2, r2_d2, G, a1, a11)
        st.success(f"λ (lambda): {lambda_value}")
        st.success(f"C (Capacitance): {C_value} µF")

# Program 5: Astable multivibrator
def program_5():
    st.header("Program 5: Astable Multivibrator")

    def calculate_frequency(R, C):
        return 1 / (1.386 * R * C)

    n = st.number_input("Enter number of times you want to calculate:", value=1, min_value=1)

    for i in range(n):
        st.subheader(f"Calculation {i + 1}")
        R = st.number_input(f"Enter resistance (R) in ohms for calculation {i + 1}:", value=0.0)
        C = st.number_input(f"Enter capacitance (C) in farads for calculation {i + 1}:", value=0.0)

        if st.button(f"Calculate Frequency for Calculation {i + 1}"):
            frequency = calculate_frequency(R, C)
            st.success(f"Frequency: {frequency:.6f} Hz")

# Program 6: Air wedge
def program_6():
    st.header("Program 6: Air Wedge")

    def compute_thickness(lambda_val, l, beta, m):
        return (lambda_val * l * m) / (2 * beta)

    lambda_val = 5893e-10  # Wavelength in meters (5893 Å)

    l = st.number_input("Enter the distance between the wire (l) in meters:", value=0.0)
    beta = st.number_input("Enter the width of the ring (β) in meters:", value=0.0)
    m = st.number_input("Enter the number of rings (m):", value=0)

    if st.button("Calculate Thickness"):
        thickness = compute_thickness(lambda_val, l, beta, m)
        st.success(f"Calculated thickness of wire (t): {thickness:.6e} meters")

# Program 7: Newton rings
def program_7():
    st.header("Program 7: Newton Rings")

    def compute_R(r_nm, r_n, m, wavelength):
        return (r_nm**2 - r_n**2) / (m * wavelength)

    wavelength = 5893e-10  # 5893 Å in meters

    r_n = st.number_input("Enter the radius of the nth ring in meters:", value=0.0)
    r_nm = st.number_input("Enter the radius of the (n+m)th ring in meters:", value=0.0)
    m = st.number_input("Enter the number of rings after nth ring (m):", value=0)

    if st.button("Compute R"):
        R_value = compute_R(r_n, r_nm, m, wavelength)
        st.success(f"Computed R value: {R_value:.5e} m⁻¹")

# Program 8: Minimum deviation
def program_8():
    st.header("Program 8: Minimum Deviation")

    def convert_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    def calculate_coefficient_of_friction(D_deg, D_min, A_deg, A_min):
        D_value = convert_to_decimal(D_deg, D_min)
        A_value = convert_to_decimal(A_deg, A_min)
        if A_value == 0:
            raise ValueError("A cannot be zero to avoid division by zero.")
        D_radians = math.radians(D_value)
        A_radians = math.radians(A_value)
        mu = math.sin((D_radians + A_radians) / 2) / math.sin(A_radians / 2)
        return mu

    n = st.number_input("Enter the number of calculations:", value=1, min_value=1)

    results = []
    for i in range(n):
        st.subheader(f"Calculation {i + 1}")
        D_deg = st.number_input(f"Enter the degrees for D (set {i + 1}):", value=0.0)
        D_min = st.number_input(f"Enter the minutes for D (set {i + 1}):", value=0.0)
        A_deg = st.number_input(f"Enter the degrees for A (set {i + 1}):", value=0.0)
        A_min = st.number_input(f"Enter the minutes for A (set {i + 1}):", value=0.0)

        if st.button(f"Calculate Coefficient of Friction for Calculation {i + 1}"):
            mu_result = calculate_coefficient_of_friction(D_deg, D_min, A_deg, A_min)
            results.append((D_deg, D_min, A_deg, A_min, mu_result))
            st.success(f"mu = {mu_result:.6f}")

    if results:
        st.subheader("Final Results")
        for i, (D_d, D_m, A_d, A_m, mu) in enumerate(results, 1):
            st.write(f"Calculation {i}:")
            st.write(f"  D = {D_d}° {D_m}'")
            st.write(f"  A = {A_d}° {A_m}'")
            st.write(f"  -> mu = {mu:.6f}")
            st.write("-" * 30)

# Program 9: Small angle prism
def program_9():
    st.header("Program 9: Small Angle Prism")

    def deg_min_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    def normal_incidence_method(A, d):
        A_rad = math.radians(A)
        d_rad = math.radians(d)
        return math.sin(A_rad + d_rad) / math.sin(A_rad)

    def normal_emergence_method(i, A):
        i_rad = math.radians(i)
        A_rad = math.radians(A)
        return math.sin(i_rad) / math.sin(A_rad)

    def minimum_deviation_method(D, A):
        D_rad = math.radians(D)
        A_rad = math.radians(A)
        return math.sin((D_rad + A_rad) / 2) / math.sin(A_rad / 2)

    method = st.selectbox("Choose a method to calculate the refractive index:", 
                          ["Normal Incidence Method", "Normal Emergence Method", "Minimum Deviation Method"])

    if method == "Normal Incidence Method":
        A_deg = st.number_input("Enter degrees for angle of prism (A):", value=0.0)
        A_min = st.number_input("Enter minutes for angle of prism (A):", value=0.0)
        A = deg_min_to_decimal(A_deg, A_min)

        d_deg = st.number_input("Enter degrees for angle of deviation (d):", value=0.0)
        d_min = st.number_input("Enter minutes for angle of deviation (d):", value=0.0)
        d = deg_min_to_decimal(d_deg, d_min)

        if st.button("Calculate Refractive Index"):
            mu = normal_incidence_method(A, d)
            st.success(f"Refractive Index (μ) using Normal Incidence Method: {mu:.6f}")

    elif method == "Normal Emergence Method":
        i_deg = st.number_input("Enter degrees for angle of incidence (i):", value=0.0)
        i_min = st.number_input("Enter minutes for angle of incidence (i):", value=0.0)
        i = deg_min_to_decimal(i_deg, i_min)

        A_deg = st.number_input("Enter degrees for angle of prism (A):", value=0.0)
        A_min = st.number_input("Enter minutes for angle of prism (A):", value=0.0)
        A = deg_min_to_decimal(A_deg, A_min)

        if st.button("Calculate Refractive Index"):
            mu = normal_emergence_method(i, A)
            st.success(f"Refractive Index (μ) using Normal Emergence Method: {mu:.6f}")

    elif method == "Minimum Deviation Method":
        D_deg = st.number_input("Enter degrees for angle of minimum deviation (D):", value=0.0)
        D_min = st.number_input("Enter minutes for angle of minimum deviation (D):", value=0.0)
        D = deg_min_to_decimal(D_deg, D_min)

        A_deg = st.number_input("Enter degrees for angle of prism (A):", value=0.0)
        A_min = st.number_input("Enter minutes for angle of prism (A):", value=0.0)
        A = deg_min_to_decimal(A_deg, A_min)

        if st.button("Calculate Refractive Index"):
            mu = minimum_deviation_method(D, A)
            st.success(f"Refractive Index (μ) using Minimum Deviation Method: {mu:.6f}")

# Program 10: Spectrometer i-i' curve
def program_10():
    st.header("Program 10: Spectrometer i-i' Curve")

    def dms_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    def calculate_mu(D, A):
        i = (D + A) / 2
        A_rad = np.radians(A)
        i_rad = np.radians(i)
        if np.sin(A_rad / 2) == 0:
            return np.nan
        mu = np.sin(i_rad) / np.sin(A_rad / 2)
        return mu

    n = st.number_input("Enter the number of values:", value=1, min_value=1)

    D_values = []
    A_values = []
    mu_values = []

    for i in range(n):
        st.subheader(f"Set {i + 1}")
        D_deg = st.number_input(f"Enter D (Deviation Angle) degrees for set {i + 1}:", value=0.0)
        D_min = st.number_input(f"Enter D (Deviation Angle) minutes for set {i + 1}:", value=0.0)
        D = dms_to_decimal(D_deg, D_min)

        A_deg = st.number_input(f"Enter A (Angle of Prism) degrees for set {i + 1}:", value=0.0)
        A_min = st.number_input(f"Enter A (Angle of Prism) minutes for set {i + 1}:", value=0.0)
        A = dms_to_decimal(A_deg, A_min)

        mu = calculate_mu(D, A)
        D_values.append(D)
        A_values.append(A)
        mu_values.append(mu)
        st.success(f"Calculated Refractive Index (μ) for set {i + 1}: {mu}")

    if st.button("Plot Results"):
        plt.figure(figsize=(5, 5))
        plt.scatter(D_values, mu_values, color='r', label='μ values')
        plt.xlabel('D (Deviation Angle in Degrees)')
        plt.ylabel('μ (Refractive Index)')
        plt.title(f'Refractive Index Calculation for {n} Values')
        plt.legend()
        plt.grid()
        st.pyplot(plt)

# Program 11: Young's modulus (Koenig method)
def program_11():
    st.header("Program 11: Young's Modulus (Koenig Method)")

    def youngs_modulus_koenig(frequency, length, width, height, density):
        I = (width * height**3) / 12
        A = width * height
        E = (2 * math.pi * frequency)**2 * (density * A * length**4) / I
        return E

    frequency = st.number_input("Enter the frequency of vibration (Hz):", value=0.0)
    length = st.number_input("Enter the length of the beam (m):", value=0.0)
    width = st.number_input("Enter the width of the beam (m):", value=0.0)
    height = st.number_input("Enter the height of the beam (m):", value=0.0)
    density = st.number_input("Enter the density of the material (kg/m³):", value=0.0)

    if st.button("Calculate Young's Modulus"):
        E = youngs_modulus_koenig(frequency, length, width, height, density)
        st.success(f"The Young's Modulus of the material is: {E:.2e} Pa")

# Program 12: Young's modulus (Non-uniform bending)
def program_12():
    st.header("Program 12: Young's Modulus (Non-uniform Bending)")

    def youngs_modulus(force, original_length, change_in_length, area):
        stress = force / area
        strain = change_in_length / original_length
        E = stress / strain
        return E

    force = st.number_input("Enter applied force (N):", value=0.0)
    original_length = st.number_input("Enter original length (m):", value=0.0)
    change_in_length = st.number_input("Enter change in length (m):", value=0.0)
    area = st.number_input("Enter cross-sectional area (m²):", value=0.0)

    if st.button("Calculate Young's Modulus"):
        E = youngs_modulus(force, original_length, change_in_length, area)
        st.success(f"Young's Modulus: {E} Pa")

# Program 13: Young's modulus (Stretching method)
def program_13():
    st.header("Program 13: Young's Modulus (Stretching Method)")

    def youngs_modulus(F, L, A, delta_L):
        if delta_L == 0:
            return "Change in length cannot be zero"
        E = (F * L) / (A * delta_L)
        return E

    F = st.number_input("Enter the applied force (N):", value=0.0)
    L = st.number_input("Enter the original length (m):", value=0.0)
    A = st.number_input("Enter the cross-sectional area (m²):", value=0.0)
    delta_L = st.number_input("Enter the change in length (m):", value=0.0)

    if st.button("Calculate Young's Modulus"):
        E = youngs_modulus(F, L, A, delta_L)
        st.success(f"Young's Modulus: {E:.2e} Pa")

# Program 14: Young's modulus (Uniform bending)
def program_14():
    st.header("Program 14: Young's Modulus (Uniform Bending)")

    def youngs_modulus_uniform_bending(m, L, b, d, y):
        g = 9.81  # Acceleration due to gravity (m/s²)
        Y = (m * g * L**3) / (4 * b * d**3 * y)
        return Y

    m = st.number_input("Enter mass (kg):", value=0.0)
    L = st.number_input("Enter length of the beam (m):", value=0.0)
    b = st.number_input("Enter breadth of the beam (m):", value=0.0)
    d = st.number_input("Enter thickness of the beam (m):", value=0.0)
    y = st.number_input("Enter depression (m):", value=0.0)

    if st.button("Calculate Young's Modulus"):
        Y = youngs_modulus_uniform_bending(m, L, b, d, y)
        st.success(f"Young's Modulus (Y) = {Y:.2e} N/m²")

# Program 15: Young's modulus (Cantilever)
def program_15():
    st.header("Program 15: Young's Modulus (Cantilever)")

    def youngs_modulus_cantilever(L, F, b, d, delta):
        E = (4 * L**3 * F) / (b * d**3 * delta)
        return E

    L = st.number_input("Enter the length of the cantilever (m):", value=0.0)
    F = st.number_input("Enter the applied force (N):", value=0.0)
    b = st.number_input("Enter the width of the beam (m):", value=0.0)
    d = st.number_input("Enter the thickness (depth) of the beam (m):", value=0.0)
    delta = st.number_input("Enter the deflection (m):", value=0.0)

    if st.button("Calculate Young's Modulus"):
        E = youngs_modulus_cantilever(L, F, b, d, delta)
        st.success(f"Young's modulus (E) = {E:.2e}")

# Program 16: Absolute mutual inductance
def program_16():
    st.header("Program 16: Absolute Mutual Inductance")

    def calculate_lambda(a1, a11):
        return 2.303 * math.log(a1 / a11)

    def calculate_M(r, T, a1, a11, d1, d2):
        lambda_value = calculate_lambda(a1, a11)
        M = (r * T / (2 * math.pi)) * (1 + lambda_value / 2) * (d1 / d2)
        return M

    r = st.number_input("Enter the fractional resistance (r):", value=0.0)
    T = st.number_input("Enter the time in seconds (T):", value=0.0)
    a1 = st.number_input("Enter the maximum distance from center for one oscillation (a1):", value=0.0)
    a11 = st.number_input("Enter the maximum distance from center for the eleventh oscillation (a11):", value=0.0)
    d1 = st.number_input("Enter the first kick in meters (d1):", value=0.0)
    d2 = st.number_input("Enter the second kick in meters (d2):", value=0.0)

    if st.button("Calculate Mutual Inductance"):
        M = calculate_M(r, T, a1, a11, d1, d2)
        st.success(f"The absolute mutual inductance (M) is: {M}")

# Program 17: Comparison of mutual inductance
def program_17():
    st.header("Program 17: Comparison of Mutual Inductance")

    def calculate_mutual_inductance_ratio(S1, S2, R1, R2):
        M1_M2_ratio = (S1 + R1) / (S2 + R2)
        return M1_M2_ratio

    S1 = st.number_input("Enter the resistance of the secondary coil S1 (in ohms):", value=0.0)
    S2 = st.number_input("Enter the resistance of the secondary coil S2 (in ohms):", value=0.0)
    R1 = st.number_input("Enter the resistance box value R1 (in ohms):", value=0.0)
    R2 = st.number_input("Enter the resistance box value R2 (in ohms):", value=0.0)

    if st.button("Calculate Ratio"):
        ratio = calculate_mutual_inductance_ratio(S1, S2, R1, R2)
        st.success(f"The ratio of M1 to M2 is: {ratio}")

# Program 18: High resistance by leakage method
def program_18():
    st.header("Program 18: High Resistance by Leakage Method")

    def calculate_resistance(C_microfarads, d1_meters, d2_meters, t_seconds):
        C_farads = C_microfarads * 1e-6
        log_term = math.log10(d1_meters / d2_meters)
        R_ohms = t_seconds / (2.303 * C_farads * log_term)
        R_mega_ohms = R_ohms * 1e-6
        return R_mega_ohms

    C_microfarads = st.number_input("Enter capacitance (C) in microfarads:", value=0.0)
    d1_meters = st.number_input("Enter distance (d1) in meters:", value=0.0)
    d2_meters = st.number_input("Enter distance (d2) in meters:", value=0.0)
    t_seconds = st.number_input("Enter time (t) in seconds:", value=0.0)

    if st.button("Calculate Resistance"):
        R_mega_ohms = calculate_resistance(C_microfarads, d1_meters, d2_meters, t_seconds)
        st.success(f"Resistance R: {R_mega_ohms} 10^6 (M)ohms")

# Program 19: Internal resistance of a cell BG
def program_19():
    st.header("Program 19: Internal Resistance of a Cell BG")

    def calculate_internal_resistance(R, d1, d2):
        B = R * (d1 - d2) / d2
        return B

    R = st.number_input("Enter the resistance box value (R):", value=0.0)
    d1 = st.number_input("Enter the kick in distance d1 (in meters):", value=0.0)
    d2 = st.number_input("Enter the kick in distance d2 (in meters):", value=0.0)

    if st.button("Calculate Internal Resistance"):
        B = calculate_internal_resistance(R, d1, d2)
        st.success(f"The internal resistance of the cell (B) is: {B}")

# Program 20: Self inductance of a coil by Anderson method
def program_20():
    st.header("Program 20: Self Inductance of a Coil by Anderson Method")

    def calculate_self_induction(C, Q, R, S, M):
        L = C * (R * Q + M * (R + S))
        return L

    C = st.number_input("Enter the condenser value (C) in microfarads:", value=0.0) * 1e-6
    Q = st.number_input("Enter the resistance box value Q (in ohms):", value=0.0)
    R = st.number_input("Enter the resistance box value R (in ohms):", value=0.0)
    S = st.number_input("Enter the resistance box value S (in ohms):", value=0.0)
    M = st.number_input("Enter the resistance box value M (in ohms):", value=0.0)

    if st.button("Calculate Self-Inductance"):
        L = calculate_self_induction(C, Q, R, S, M)
        st.success(f"The self-induction L is: {L} Henry")

# Main function to run the app
def main():
    st.title("Physics Programs")
    program_choice = st.sidebar.selectbox(
        "Select a program:",
        [
            "Program 1: Polarimeter",
            "Program 2: Calibration of a High Range Voltmeter",
            "Program 3: Sonometer",
            "Program 4: BG Absolute Capacity of a Condenser",
            "Program 5: Astable Multivibrator",
            "Program 6: Air Wedge",
            "Program 7: Newton Rings",
            "Program 8: Minimum Deviation",
            "Program 9: Small Angle Prism",
            "Program 10: Spectrometer i-i' Curve",
            "Program 11: Young's Modulus (Koenig Method)",
            "Program 12: Young's Modulus (Non-uniform Bending)",
            "Program 13: Young's Modulus (Stretching Method)",
            "Program 14: Young's Modulus (Uniform Bending)",
            "Program 15: Young's Modulus (Cantilever)",
            "Program 16: Absolute Mutual Inductance",
            "Program 17: Comparison of Mutual Inductance",
            "Program 18: High Resistance by Leakage Method",
            "Program 19: Internal Resistance of a Cell BG",
            "Program 20: Self Inductance of a Coil by Anderson Method"
        ]
    )

    if program_choice == "Program 1: Polarimeter":
        program_1()
    elif program_choice == "Program 2: Calibration of a High Range Voltmeter":
        program_2()
    elif program_choice == "Program 3: Sonometer":
        program_3()
    elif program_choice == "Program 4: BG Absolute Capacity of a Condenser":
        program_4()
    elif program_choice == "Program 5: Astable Multivibrator":
        program_5()
    elif program_choice == "Program 6: Air Wedge":
        program_6()
    elif program_choice == "Program 7: Newton Rings":
        program_7()
    elif program_choice == "Program 8: Minimum Deviation":
        program_8()
    elif program_choice == "Program 9: Small Angle Prism":
        program_9()
    elif program_choice == "Program 10: Spectrometer i-i' Curve":
        program_10()
    elif program_choice == "Program 11: Young's Modulus (Koenig Method)":
        program_11()
    elif program_choice == "Program 12: Young's Modulus (Non-uniform Bending)":
        program_12()
    elif program_choice == "Program 13: Young's Modulus (Stretching Method)":
        program_13()
    elif program_choice == "Program 14: Young's Modulus (Uniform Bending)":
        program_14()
    elif program_choice == "Program 15: Young's Modulus (Cantilever)":
        program_15()
    elif program_choice == "Program 16: Absolute Mutual Inductance":
        program_16()
    elif program_choice == "Program 17: Comparison of Mutual Inductance":
        program_17()
    elif program_choice == "Program 18: High Resistance by Leakage Method":
        program_18()
    elif program_choice == "Program 19: Internal Resistance of a Cell BG":
        program_19()
    elif program_choice == "Program 20: Self Inductance of a Coil by Anderson Method":
        program_20()

if __name__ == "__main__":
    main()
