import math
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

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

def program_1():
    # inputs
    theta_deg = int(input("Enter θ/c degrees: "))
    theta_min = float(input("Enter θ/c minutes: "))
    l = float(input("Enter l (in meter): "))

    result_d, result_m, result_s = calculate_value(theta_deg, theta_min, l)
    print(f"Calculated Value: {result_d}° {result_m}' {result_s}\"")

    # Error calculation
    standard_deg = int(input("Enter standard value degrees: "))
    standard_min = float(input("Enter standard value minutes: "))
    observed_deg = int(input("Enter observed value degrees: "))
    observed_min = float(input("Enter observed value minutes: "))

    error_percent = calculate_error_percentage(standard_deg, standard_min, observed_deg, observed_min)
    print(f"Error Percentage: {error_percent}%")

def program_2():
    # Input: Number of times to calculate
    n = int(input("Enter the number of calculations: "))

    # Enter l1 once
    l1 = float(input("Enter l1: "))  

    # Lists to store values
    V_list = []
    l2_list = []
    V_prime_list = []
    correction_list = []

    # Loop to calculate V' and correction
    for i in range(n):
        print(f"\n--- Calculation {i+1} ---")
        V = float(input("Enter V: "))  # Get V from user
        l2 = float(input("Enter l2: "))  # Get l2 from user

        V_prime = 50 * 1.08 * l2 / l1  # Formula for V'
        correction = V_prime - V  # Correction calculation

        # Store values in lists
        V_list.append(V)
        l2_list.append(l2)
        V_prime_list.append(V_prime)
        correction_list.append(correction)

    # Create tabular data
    table_data = []
    for i in range(n):
        table_data.append([V_list[i], l2_list[i], V_prime_list[i], correction_list[i]])

    # Print table
    headers = ["Voltmeter readings", "l2", "V' (Calculated Voltage)", "Correction (V' - V)"]
    print("\nResults:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # *Graph 1: V vs. Correction (V' - V)*
    plt.figure(figsize=(8, 5))
    plt.scatter(V_list, correction_list, color='red', marker='o', label="Correction (V' - V)")
    plt.plot(V_list, correction_list, linestyle='--', alpha=0.7, color='red')
    plt.xlabel("V")
    plt.ylabel("V' - V (Correction)")
    plt.title("Graph 1: V vs. Correction")
    plt.legend()
    plt.grid(True)

    # *Graph 2: V vs. V'*
    plt.figure(figsize=(8, 5))
    plt.scatter(V_list, V_prime_list, color='blue', marker='o', label="V'")
    plt.plot(V_list, V_prime_list, linestyle='--', alpha=0.7, color='blue')
    plt.xlabel("V")
    plt.ylabel("V'")
    plt.title("Graph 2: V vs. V'")
    plt.legend()
    plt.grid(True)

    # Show the graphs
    plt.show()

def program_3():
    def calculate_mass_of_wire(r, rho):
        """Calculate mass per unit length (m) using m = π(r^2)ρ."""
        return math.pi * (r ** 2) * rho

    def calculate_frequency(M, g, r, rho):
        """Calculate the frequency of the tuning fork."""
        mass_of_wire = calculate_mass_of_wire(r, rho)
        frequency = (1 / 2) * math.sqrt((M * g) / mass_of_wire)
        return frequency

    # Taking user input
    M = eval(input("Enter the mass/length^2(M/l² ) in kg/m² : "))
    g = 9.81  # Acceleration due to gravity in m/s^2
    r = float(input("Enter the radius of the wire (r) in meters: "))  
    rho = float(input("Enter the density of the wire (ρ) in kg/m^3: "))  

    # Calculating frequency
    frequency = calculate_frequency(M, g, r, rho)

    # Display result
    print(f"Frequency of the tuning fork: {frequency:.2f} Hz")

def program_4():
    def calculate_C(T, d1_R2, r2_d2, G, a1, a11):
        # Calculate lambda and round to 4 decimal places
        lambda_value = round((2.303 / 10) * math.log10(a1 / a11), 4)
        
        # Calculate C in Farads (keeping full precision)
        C = (T / (2 * math.pi * G)) * d1_R2 * r2_d2 * (1 + (lambda_value / 2))
        
        # Convert C to microfarads (1 F = 10^6 µF) before rounding
        C_microfarad = round(C * 1e6, 4)
        
        return lambda_value, C_microfarad

    # Example usage
    T = float(input("Enter T: "))
    d1_R2 = eval(input("Enter d1/R2: "))
    r2_d2 = float(input("Enter r2/d2: "))
    G = float(input("Enter G: "))
    a1 = float(input("Enter a1: "))
    a11 = float(input("Enter a11: "))

    lambda_value, C_value = calculate_C(T, d1_R2, r2_d2, G, a1, a11)

    # Display results
    print(f"λ (lambda): {lambda_value}")
    print(f"C (Capacitance): {C_value} µF")

def program_5():
    def calculate_frequency(R, C):
        return 1 / (1.386 * R * C)

    # Ask for the number of repetitions
    n = int(input("Enter number of times you wanna calculate: "))

    # Run the loop for n times
    for i in range(n):
        print(f"\nCalculation {i + 1} of {n}:")
        
        # Taking user inputs with support for scientific notation
        R = eval(input("Enter resistance (R) in ohms: "))
        C = eval(input("Enter capacitance (C) in farads: "))

        # Calculate and display frequency
        frequency = calculate_frequency(R, C)
        print(f"Frequency: {frequency:.6f} Hz")

def program_6():
    # Function to compute the thickness of the wire
    def compute_thickness(lambda_val, l, beta, m):
        return (lambda_val * l * m) / (2 * beta)

    # Constants
    lambda_val = 5893e-10  # Wavelength in meters (5893 Å)

    while True:
        try:
            # User inputs
            l = float(input("Enter the distance between the wire (l) in meters: ").strip())
            beta = float(input("Enter the width of the ring (β) in meters: ").strip())
            m = int(input("Enter the number of rings (m): ").strip())

            # Validate inputs
            if l <= 0 or beta <= 0 or m <= 0:
                raise ValueError("All values must be positive numbers.")

            # Compute thickness
            thickness = compute_thickness(lambda_val, l, beta, m)

            # Display output
            print("\n--- Results ---")
            print(f"Wavelength (λ): {lambda_val} meters")
            print(f"Distance between wire (l): {l} meters")
            print(f"Width of ring (β): {beta} meters")
            print(f"Number of rings (m): {m}")
            print(f"Calculated thickness of wire (t): {thickness:.6e} meters\n")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Ask if the user wants to continue
        choice = input("Do you want to compute another value? (yes/no): ").strip().lower()
        if choice not in ["yes", "y"]:
            print("Exiting program. Goodbye!")
            break

def program_7():
    def compute_R(r_nm, r_n, m, wavelength):
        return (r_nm**2 - r_n**2) / (m * wavelength)

    # Given wavelength in meters (5893 Å)
    wavelength = 5893e-10  # 5893 Å in meters

    while True:
        try:
            # Taking input values
            r_n = float(input("Enter the radius of the nth ring in meters: ").strip())
            r_nm = float(input("Enter the radius of the (n+m)th ring in meters: ").strip())
            m = int(input("Enter the number of rings after nth ring (m): ").strip())

            # Validations
            if r_nm <= 0 or r_n <= 0 or m <= 0:
                print("Error: Radii and m must be positive values. Try again.")
                continue
            if r_nm <= r_n:
                print("Error: r_nm must be greater than r_n. Try again.")
                continue

            # Compute R
            R_value = compute_R(r_n, r_nm, m, wavelength)

            # Print formatted output
            print(f"Computed R value: {R_value:.5e} m⁻¹")

        except ValueError:
            print("Error: Please enter valid numerical values. Try again.")
            continue

        # Ask if the user wants to continue
        choice = input("Do you want to compute another value? (yes/no): ").strip().lower()
        if choice not in ["yes", "y"]:
            print("Exiting program. Goodbye!")
            break

def program_8():
    # Function to convert degrees and minutes to decimal degrees
    def convert_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    # Function to compute the coefficient of friction (mu)
    def calculate_coefficient_of_friction(D_deg, D_min, A_deg, A_min):
        # Convert D and A to decimal degrees
        D_value = convert_to_decimal(D_deg, D_min)
        A_value = convert_to_decimal(A_deg, A_min)
        
        if A_value == 0:
            raise ValueError("A cannot be zero to avoid division by zero.")
        
        # Convert degrees to radians for calculations
        D_radians = math.radians(D_value)
        A_radians = math.radians(A_value)
        
        # Apply the formula
        mu = math.sin((D_radians + A_radians) / 2) / math.sin(A_radians / 2)
        return mu

    # Main script
    try:
        n = int(input("Enter the number of calculations: "))
        
        results = []
        for i in range(n):
            print(f"\n--- Calculation {i+1} ---")
            try:
                # Get degrees and minutes for D
                D_deg = float(input(f"Enter the degrees for D (set {i+1}): "))
                D_min = float(input(f"Enter the minutes for D (set {i+1}): "))

                # Get degrees and minutes for A
                A_deg = float(input(f"Enter the degrees for A (set {i+1}): "))
                A_min = float(input(f"Enter the minutes for A (set {i+1}): "))

                mu_result = calculate_coefficient_of_friction(D_deg, D_min, A_deg, A_min)
                results.append((D_deg, D_min, A_deg, A_min, mu_result))

            except ValueError as e:
                print(f"Invalid input: {e}")

        # Display results with breaks
        print("\n======= Final Results =======")
        for i, (D_d, D_m, A_d, A_m, mu) in enumerate(results, 1):
            print(f"\nCalculation {i}:")
            print(f"  D = {D_d}° {D_m}'")
            print(f"  A = {A_d}° {A_m}'")
            print(f"  -> mu = {mu:.6f}")
            print("-" * 30)  # Adds a separator line

    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of calculations.")

def program_9():
    # Function to convert degrees and minutes to decimal degrees
    def deg_min_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    # Function to compute refractive index using the Normal Incidence Method
    def normal_incidence_method(A, d):
        A_rad = math.radians(A)
        d_rad = math.radians(d)
        return math.sin(A_rad + d_rad) / math.sin(A_rad)

    # Function to compute refractive index using the Normal Emergence Method
    def normal_emergence_method(i, A):
        i_rad = math.radians(i)
        A_rad = math.radians(A)
        return math.sin(i_rad) / math.sin(A_rad)

    # Function to compute refractive index using the Minimum Deviation Method
    def minimum_deviation_method(D, A):
        D_rad = math.radians(D)
        A_rad = math.radians(A)
        return math.sin((D_rad + A_rad) / 2) / math.sin(A_rad / 2)

    # Main program loop
    while True:
        print("\nChoose a method to calculate the refractive index:")
        print("1. Normal Incidence Method")
        print("2. Normal Emergence Method")
        print("3. Minimum Deviation Method")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            # Input for angle of prism (A)
            A_deg = int(input("Enter degrees for angle of prism (A): "))
            A_min = float(input("Enter minutes for angle of prism (A): "))
            A = deg_min_to_decimal(A_deg, A_min)

            # Input for angle of deviation (d)
            d_deg = int(input("Enter degrees for angle of deviation (d): "))
            d_min = float(input("Enter minutes for angle of deviation (d): "))
            d = deg_min_to_decimal(d_deg, d_min)

            mu = normal_incidence_method(A, d)
            print(f"Refractive Index (μ) using Normal Incidence Method: {mu:.6f}")

        elif choice == "2":
            # Input for angle of incidence (i)
            i_deg = int(input("Enter degrees for angle of incidence (i): "))
            i_min = float(input("Enter minutes for angle of incidence (i): "))
            i = deg_min_to_decimal(i_deg, i_min)

            # Input for angle of prism (A)
            A_deg = int(input("Enter degrees for angle of prism (A): "))
            A_min = float(input("Enter minutes for angle of prism (A): "))
            A = deg_min_to_decimal(A_deg, A_min)

            mu = normal_emergence_method(i, A)
            print(f"Refractive Index (μ) using Normal Emergence Method: {mu:.6f}")

        elif choice == "3":
            # Input for angle of minimum deviation (D)
            D_deg = int(input("Enter degrees for angle of minimum deviation (D): "))
            D_min = float(input("Enter minutes for angle of minimum deviation (D): "))
            D = deg_min_to_decimal(D_deg, D_min)

            # Input for angle of prism (A)
            A_deg = int(input("Enter degrees for angle of prism (A): "))
            A_min = float(input("Enter minutes for angle of prism (A): "))
            A = deg_min_to_decimal(A_deg, A_min)

            mu = minimum_deviation_method(D, A)
            print(f"Refractive Index (μ) using Minimum Deviation Method: {mu:.6f}")

        elif choice == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")

        # Ask if the user wants to continue
        choice = input("\nDo you want to compute another value? (yes/no): ").strip().lower()
        if choice not in ["yes", "y"]:
            print("Exiting program. Goodbye!")
            break

def program_10():
    def dms_to_decimal(degrees, minutes):
        return degrees + (minutes / 60)

    def calculate_mu(D, A):
        i = (D + A) / 2  # Compute i
        A_rad = np.radians(A)  # Convert A to radians
        i_rad = np.radians(i)  # Convert i to radians
        
        if np.sin(A_rad / 2) == 0:
            return np.nan  # Avoid division by zero
        
        mu = np.sin(i_rad) / np.sin(A_rad / 2)  # Compute mu
        return mu

    # User will input multiple values for D and A in a single entry
    n = int(input("Enter the number of values: "))
    D_values = []
    A_values = []
    mu_values = []

    print("Enter values in the format: degrees minutes ")

    for i in range(n):
        D_deg, D_min = map(float, input(f"Enter D (Deviation Angle) for set {i+1}: ").split())
        A_deg, A_min = map(float, input(f"Enter A (Angle of Prism) for set {i+1}: ").split())
        
        D = dms_to_decimal(D_deg, D_min)
        A = dms_to_decimal(A_deg, A_min)
        
        mu = calculate_mu(D, A)
        
        D_values.append(D)
        A_values.append(A)
        mu_values.append(mu)
        
        print(f"Calculated Refractive Index (μ) for set {i+1}: {mu}")

    # Plot the results
    plt.figure(figsize=(5, 5))
    plt.scatter(D_values, mu_values, color='r', label='μ values')
    plt.xlabel('D (Deviation Angle in Degrees)')
    plt.ylabel('μ (Refractive Index)')
    plt.title(f'Refractive Index Calculation for {n} Values')
    plt.legend()
    plt.grid()
    plt.show()

def program_11():
    def youngs_modulus_koenig(frequency, length, width, height, density):
        # Second moment of area for a rectangular beam (I = b * h^3 / 12)
        I = (width * height**3) / 12
        
        # Cross-sectional area of the beam (A = b * h)
        A = width * height
        
        # Calculating Young's Modulus using Koenig's method formula
        E = (2 * math.pi * frequency)*2 * (density * A * length*4) / I
        
        return E

    # Input values
    frequency = float(input("Enter the frequency of vibration (Hz): "))
    length = float(input("Enter the length of the beam (m): "))
    width = float(input("Enter the width of the beam (m): "))
    height = float(input("Enter the height of the beam (m): "))
    density = float(input("Enter the density of the material (kg/m³): "))

    # Calculate Young's Modulus
    E = youngs_modulus_koenig(frequency, length, width, height, density)

    # Output the result
    print(f"The Young's Modulus of the material is: {E:.2e} Pa")

def program_12():
    def youngs_modulus(force, original_length, change_in_length, area):
        # Calculate stress
        stress = force / area
        
        # Calculate strain
        strain = change_in_length / original_length
        
        # Calculate Young's modulus
        E = stress / strain
        return E

    # Example values
    force = float(input("Enter applied force (N): "))
    original_length = float(input("Enter original length (m): "))
    change_in_length = float(input("Enter change in length (m): "))
    area = float(input("Enter cross-sectional area (m²): "))

    # Calculate and display Young's modulus
    E = youngs_modulus(force, original_length, change_in_length, area)
    print(f"Young's Modulus: {E} Pa")

def program_13():
    def youngs_modulus(F, L, A, delta_L):
        if delta_L == 0:
            return "Change in length cannot be zero"
        
        E = (F * L) / (A * delta_L)
        return E

    # Example values
    F = float(input("Enter the applied force (N): "))
    L = float(input("Enter the original length (m): "))
    A = float(input("Enter the cross-sectional area (m²): "))
    delta_L = float(input("Enter the change in length (m): "))

    E = youngs_modulus(F, L, A, delta_L)

    print(f"Young's Modulus: {E:.2e} Pa")  # Scientific notation format

def program_14():
    def youngs_modulus_uniform_bending():
        print("Young's Modulus Calculation - Uniform Bending")
        
        # Input values
        m = float(input("Enter mass (kg): "))
        L = float(input("Enter length of the beam (m): "))
        b = float(input("Enter breadth of the beam (m): "))
        d = float(input("Enter thickness of the beam (m): "))
        y = float(input("Enter depression (m): "))

        g = 9.81  # Acceleration due to gravity (m/s²)

        # Calculation
        Y = (m * g * L*3) / (4 * b * d*3 * y)

        # Display result
        print(f"Young's Modulus (Y) = {Y:.2e} N/m²")

    # Run the function
    if __name__ == "__main__":
        youngs_modulus_uniform_bending()

def program_15():
    def youngs_modulus_cantilever(L, F, b, d, delta):
        E = (4 * L*3 * F) / (b * d*3 * delta)
        return E

    # Input values
    L = float(input("Enter the length of the cantilever (m): "))
    F = float(input("Enter the applied force (N): "))
    b = float(input("Enter the width of the beam (m): "))
    d = float(input("Enter the thickness (depth) of the beam (m): "))
    delta = float(input("Enter the deflection (m): "))

    # Calculate Young's modulus
    E = youngs_modulus_cantilever(L, F, b, d, delta)

    print(f"Young's modulus (E) = {E:.2e}")

def program_16():
    def calculate_lambda(a1, a11):
        return 2.303 * math.log(a1 / a11)

    def calculate_M(r, T, a1, a11, d1, d2):
        lambda_value = calculate_lambda(a1, a11)
        M = (r * T / (2 * math.pi)) * (1 + lambda_value / 2) * (d1 / d2)
        return M

    while True:
        
        r = float(input("Enter the fractional resistance (r): "))
        T = float(input("Enter the time in seconds (T): "))
        a1 = float(input("Enter the maximum distance from center for one oscillation (a1): "))
        a11 = float(input("Enter the maximum distance from center for the eleventh oscillation (a11): "))
        d1 = float(input("Enter the first kick in meters (d1): "))
        d2 = float(input("Enter the second kick in meters (d2): "))

        M = calculate_M(r, T, a1, a11, d1, d2)
        print(f"The absolute mutual inductance (M) is: {M}")

        again = input("Press 'Enter' to run again or type 'exit' to stop: ").strip()
        if again.lower() == 'exit':
            break

def program_17():
    def calculate_mutual_inductance_ratio(S1, S2, R1, R2):
        M1_M2_ratio = (S1 + R1) / (S2 + R2)
        return M1_M2_ratio

    while True:
        
        S1 = float(input("Enter the resistance of the secondary coil S1 (in ohms): "))
        S2 = float(input("Enter the resistance of the secondary coil S2 (in ohms): "))
        R1 = float(input("Enter the resistance box value R1 (in ohms): "))
        R2 = float(input("Enter the resistance box value R2 (in ohms): "))
    
        ratio = calculate_mutual_inductance_ratio(S1, S2, R1, R2)
        print(f"The ratio of M1 to M2 is: {ratio}")

        again = input("Press 'Enter' to run again or type 'exit' to stop: ").strip()
        if again.lower() == 'exit':
            break

def program_18():
    def calculate_resistance(C_microfarads, d1_meters, d2_meters, t_seconds):
        
        C_farads = C_microfarads * 1e-6
        
        
        log_term = math.log10(d1_meters / d2_meters)
        
        
        R_ohms = t_seconds / (2.303 * C_farads * log_term)
        
        
        R_mega_ohms = R_ohms * 1e-6
        
        return R_mega_ohms

    C_microfarads = float(input("Enter capacitance (C) in microfarads: "))
    d1_meters = float(input("Enter distance (d1) in meters: "))
    d2_meters = float(input("Enter distance (d2) in meters: "))
    t_seconds = float(input("Enter time (t) in seconds: "))

    R_mega_ohms = calculate_resistance(C_microfarads, d1_meters, d2_meters, t_seconds)
    print(f"Resistance R: {R_mega_ohms} 10^6 (M)ohms")

def program_19():
    def calculate_internal_resistance(R, d1, d2):
        B = R * (d1 - d2) / d2
        return B

    while True:
        # Get input values from the user
        R = float(input("Enter the resistance box value (R): "))
        d1 = float(input("Enter the kick in distance d1 (in meters): "))
        d2 = float(input("Enter the kick in distance d2 (in meters): "))

        # Calculate and display the internal resistance B
        B = calculate_internal_resistance(R, d1, d2)
        print(f"The internal resistance of the cell (B) is: {B}")

        # Ask the user if they want to run the code again
        again = input("Press 'Enter' to run again or type 'exit' to stop: ").strip()
        if again.lower() == 'exit':
            break

def program_20():
    def calculate_self_induction(C, Q, R, S, M):
        L = C * (R * Q + M * (R + S))
        return L

    while True:
        
        C = float(input("Enter the condenser value (C) in microfarads: ")) * 10**(-6)
        Q = float(input("Enter the resistance box value Q (in ohms): "))
        R = float(input("Enter the resistance box value R (in ohms): "))
        S = float(input("Enter the resistance box value S (in ohms): "))
        M = float(input("Enter the resistance box value M (in ohms): "))

        L = calculate_self_induction(C, Q, R, S, M)
        print(f"The self-induction L is: {L} Henry")

        again = input("Press 'Enter' to run again or type 'exit' to stop: ").strip()
        if again.lower() == 'exit':
            break

def main():
    print("Select a program to run:")
    print("1. Spectrometer")
    print("2. Calibration of a high range voltmeter")
    print("3. Sonometer")
    print("4. BG absolute capacity of a condenser")
    print("5. Astable multivibrator")
    print("6. Air wedge")
    print("7. Newton rings")
    print("8. Minimum deviation")
    print("9. Small angle prism")
    print("10. Spectrometer i-i' curve")
    print("11. Young's modulus (Koenig method)")
    print("12. Young's modulus (Non-uniform bending)")
    print("13. Young's modulus (Stretching method)")
    print("14. Young's modulus (Uniform bending)")
    print("15. Young's modulus (Cantilever)")
    print("16. Absolute mutual inductance")
    print("17. Comparison of mutual inductance")
    print("18. High resistance by leakage method")
    print("19. Internal resistance of a cell BG")
    print("20. Self inductance of a coil by Anderson method")

    choice = int(input("Enter the number of the program you want to run: "))

    if choice == 1:
        program_1()
    elif choice == 2:
        program_2()
    elif choice == 3:
        program_3()
    elif choice == 4:
        program_4()
    elif choice == 5:
        program_5()
    elif choice == 6:
        program_6()
    elif choice == 7:
        program_7()
    elif choice == 8:
        program_8()
    elif choice == 9:
        program_9()
    elif choice == 10:
        program_10()
    elif choice == 11:
        program_11()
    elif choice == 12:
        program_12()
    elif choice == 13:
        program_13()
    elif choice == 14:
        program_14()
    elif choice == 15:
        program_15()
    elif choice == 16:
        program_16()
    elif choice == 17:
        program_17()
    elif choice == 18:
        program_18()
    elif choice == 19:
        program_19()
    elif choice == 20:
        program_20()
    else:
        print("Invalid choice. Please select a number between 1 and 20.")

if __name__ == "__main__":
    main()
