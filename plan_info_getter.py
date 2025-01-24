import os
import pydicom
import csv

def extract_dicom_info(directory):
    # Define the output CSV file path
    output_csv = os.path.join(directory, "dicom_info_output.csv")

    # Initialize a list to hold the extracted information
    data = []

    # Walk through the directory
    for root, _, files in os.walk(directory):
        # Check if PL001.dcm exists in the current folder
        if "PL001.dcm" in files:
            dicom_file_path = os.path.join(root, "PL001.dcm")

            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(dicom_file_path)

                # Extract required tags
                subfolder_name = os.path.basename(root)
                patient_name = dicom_data.get((0x0010, 0x0010), "Unknown").value if (0x0010, 0x0010) in dicom_data else "Unknown"
                patient_id = dicom_data.get((0x0010, 0x0020), "Unknown").value if (0x0010, 0x0020) in dicom_data else "Unknown"
                target_prescription_dose = dicom_data.get((0x300A, 0x0026), "Unknown").value if (0x300A, 0x0026) in dicom_data else "Unknown"
                brachy_application_setups = dicom_data.get((0x300A, 0x00A0), "Unknown").value if (0x300A, 0x00A0) in dicom_data else "Unknown"

                # Append the data
                data.append([subfolder_name, patient_name, patient_id, target_prescription_dose, brachy_application_setups])

            except Exception as e:
                print(f"Error reading {dicom_file_path}: {e}")

    # Write the collected data to the CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Subfolder Name", "Patient Name", "Patient ID", "Target Prescription Dose", "Number of Brachy Application Setups"])
        # Write the data rows
        writer.writerows(data)

    print(f"Output written to {output_csv}")

# Replace with the target directory path
directory = r"H:\\CCSI\\PlanningModule\\Brachy Projects\\1. CIHR MDBC Collaboration\\Prostate Patients\\Prostate Patients (Dakota 2022-2020)"
extract_dicom_info(directory)