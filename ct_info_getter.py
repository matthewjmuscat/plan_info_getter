import os
import pydicom
import csv

def extract_ct_dicom_info(directory):
    # Define the output CSV file path
    output_csv = os.path.join(directory, "ct_dicom_info_output.csv")

    # Initialize a list to hold the extracted information
    data = []

    # Walk through the directory
    for root, _, files in os.walk(directory):
        # Check if CT001.dcm and CT002.dcm exist in the current folder
        if "CT001.dcm" in files and "CT002.dcm" in files:
            ct1_path = os.path.join(root, "CT001.dcm")
            ct2_path = os.path.join(root, "CT002.dcm")

            try:
                # Read the CT001.dcm file
                ct1_data = pydicom.dcmread(ct1_path)
                
                # Read the CT002.dcm file for slice thickness calculation
                ct2_data = pydicom.dcmread(ct2_path)

                # Extract required tags from CT001
                subfolder_name = os.path.basename(root)
                patient_name = ct1_data.get((0x0010, 0x0010), "Unknown").value if (0x0010, 0x0010) in ct1_data else "Unknown"
                patient_id = ct1_data.get((0x0010, 0x0020), "Unknown").value if (0x0010, 0x0020) in ct1_data else "Unknown"
                
                # Extract pixel spacing (0028,0030)
                pixel_spacing = ct1_data.get((0x0028, 0x0030), ["Unknown", "Unknown"]).value if (0x0028, 0x0030) in ct1_data else ["Unknown", "Unknown"]
                pixel_spacing_x = pixel_spacing[0] if len(pixel_spacing) > 0 else "Unknown"
                pixel_spacing_y = pixel_spacing[1] if len(pixel_spacing) > 1 else "Unknown"

                # Extract Image Position (Patient) (0020,0032) from both CT001 and CT002
                position_ct1 = ct1_data.get((0x0020, 0x0032), ["Unknown", "Unknown", "Unknown"]).value
                position_ct2 = ct2_data.get((0x0020, 0x0032), ["Unknown", "Unknown", "Unknown"]).value

                # Calculate slice thickness
                if position_ct1 != "Unknown" and position_ct2 != "Unknown":
                    slice_thickness = abs(float(position_ct2[2]) - float(position_ct1[2]))
                else:
                    slice_thickness = "Unknown"

                # Append the data
                data.append([
                    subfolder_name,
                    patient_name,
                    patient_id,
                    pixel_spacing_x,
                    pixel_spacing_y,
                    slice_thickness
                ])

            except Exception as e:
                print(f"Error processing files in {root}: {e}")

    # Write the collected data to the CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Subfolder Name", "Patient Name", "Patient ID", "Pixel Spacing X", "Pixel Spacing Y", "Slice Thickness"])
        # Write the data rows
        writer.writerows(data)

    print(f"Output written to {output_csv}")

# Replace with the target directory path
directory = r"H:\\CCSI\\PlanningModule\\Brachy Projects\\1. CIHR MDBC Collaboration\\Prostate Patients\\Prostate Patients (Dakota 2022-2020)"
extract_ct_dicom_info(directory)