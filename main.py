import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

# Use 'Agg' backend for non-interactive environments
matplotlib.use('Agg')

CSV_FILE = "client_data.csv"
GRAPH_FILE = "carbon_trends.png"

# Function to calculate carbon footprint based on input data
def calculate_footprint(energy, distance, waste):
    """
    Calculate the total carbon footprint based on energy, transport, and waste.
    """
    return energy * 0.233 + distance * 0.12 + waste * 0.5

# Function to append client data to a CSV file
def append_to_csv(client_data):
    """
    Append new client data to the CSV file. If the file doesn't exist, create it.
    """
    df = pd.DataFrame([client_data])
    
    # Append to existing file, else create a new file with headers
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, mode='w', header=True, index=False)

    print(f"Data for {client_data['Client']} added to CSV.")

# Function to generate a trend graph from CSV data
def generate_graph():
    if not os.path.exists(CSV_FILE):
        print("No data found! Run the program and add client data first.")
        return

    # Load client data
    df = pd.read_csv(CSV_FILE)

    # Print the column names for debugging
    print("CSV Columns:", df.columns)

    if 'Client' not in df.columns:
        print("Error: 'Client' column not found in CSV.")
        return

    # Proceed with plotting
    plt.figure(figsize=(10, 6))
    plt.bar(df['Client'], df['total_footprint'], color='skyblue', label='Carbon Footprint')
    plt.plot(df['Client'], df['energy_kwh'], color='green', marker='o', label='Energy', linestyle='--')
    plt.plot(df['Client'], df['transport_km'], color='orange', marker='o', label='Transport', linestyle='--')
    plt.plot(df['Client'], df['waste_kg'], color='red', marker='o', label='Waste', linestyle='--')

    plt.xlabel('Clients')
    plt.ylabel('Metrics')
    plt.title('Carbon Footprint Trends')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.legend()

    plt.savefig(GRAPH_FILE, dpi=300)
    plt.close()
    print(f"Graph saved as '{GRAPH_FILE}'.")

# Function to create a PDF report for each client
def create_report(data, file_path):
    """
    Generates a PDF report for a given client's data.
    Also includes the comparative PNG graph if it exists.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    pdf = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 40, "Carbon Footprint Report")

    pdf.setFont("Helvetica", 12)
    y_position = height - 80

    # Client data
    pdf.drawString(50, y_position, f"Client: {data['Client']}")
    y_position -= 20
    pdf.drawString(50, y_position, f"Energy: {data['energy_kwh']} kWh")
    y_position -= 20
    pdf.drawString(50, y_position, f"Transport: {data['transport_km']} km")
    y_position -= 20
    pdf.drawString(50, y_position, f"Waste: {data['waste_kg']} kg")
    y_position -= 20
    pdf.drawString(50, y_position, f"Footprint: {data['total_footprint']} kg CO2")
    y_position -= 30

    # Suggestions for reducing carbon footprint
    pdf.drawString(50, y_position, "Suggestions:")
    y_position -= 20
    pdf.drawString(50, y_position, "- Use energy-efficient appliances.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Carpool or use public transport.")
    y_position -= 15
    pdf.drawString(50, y_position, "- Recycle and reduce waste.")
    y_position -= 40

    # Add graph if available
    if os.path.exists(GRAPH_FILE):
        pdf.drawString(50, y_position, "Carbon Footprint Comparison Graph:")
        y_position -= 200
        pdf.drawImage(GRAPH_FILE, 50, y_position, width=500, height=200, preserveAspectRatio=True)
        print(f"Added {GRAPH_FILE} to {file_path}")

    # Save PDF
    pdf.save()
    print(f"PDF Report Created: {file_path}")

# Main function to collect input, update CSV, generate graph, and create reports
def main():
    """
    Main function to handle user input and generate reports for multiple clients.
    Data is stored in a CSV file, and a comparative graph is generated from the stored data.
    """
    client_data = []

    while True:
        print("\nEnter client data:")
        
        # Input validation
        try:
            energy_kwh = float(input("Energy (kWh): "))
            transport_km = float(input("Transport (km): "))
            waste_kg = float(input("Waste (kg): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        # Calculate total footprint
        total_footprint = calculate_footprint(energy_kwh, transport_km, waste_kg)

        # Get client name
        client_name = input("Client Name: ")

        # Store client details
        client_details = {
            'Client': client_name,
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'waste_kg': waste_kg,
            'total_footprint': total_footprint
        }
        
        # Append client data to list & CSV
        client_data.append(client_details)
        append_to_csv(client_details)

        # Ask if user wants to add another client
        continue_input = input("Add another client? (yes/no): ").strip().lower()
        if continue_input != 'yes':
            break

    # Generate PNG Graph from CSV data before creating reports
    generate_graph()

    # Create individual reports for each client
    for client in client_data:
        report_filename = f"Reports/{client['Client']}_report.pdf"
        create_report(client, report_filename)

    print("All reports generated successfully.")

# Run the main function
if __name__ == "__main__":
    main()
