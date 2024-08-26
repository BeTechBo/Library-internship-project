import cv2
import face_recognition
import pytesseract
import csv
import re
import os
import sys
import glob
import shutil
import pandas as pd
import numpy as np



def crop_upper_sections(image_path, output_folder):
    """Crops the upper part of the image into 6 sections.

    Args:
        image_path (str): Path to the input image.
        output_folder (str): Path to save cropped images.
        crop_left (int, optional): Amount to crop from the left. Defaults to 0.
        crop_right (int, optional): Amount to crop from the right. Defaults to 0.
        crop_top (int, optional): Amount to crop from the top. Defaults to 0.
        crop_bottom (int, optional): Amount to crop from the bottom. Defaults to 0.
    """
    
    # Adjust these values as needed
    crop_left = 60  
    crop_right = 50 
    crop_top = 50
    crop_bottom = 0 

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at {image_path}")
        return

    height, width, _ = image.shape

    # Crop the image first
    cropped_image = image[crop_top:height - crop_bottom, crop_left:width - crop_right]
    
    # Now work with the cropped image
    height, width, _ = cropped_image.shape 
    section_height = height // 2  # Upper half of the image
    upper_region = cropped_image[:section_height, :] # Select upper region

    section_width = width // 3

    for i in range(3):
        for j in range(2):
            left = i * section_width
            top = j * (section_height // 2) 
            right = left + section_width
            bottom = top + (section_height // 2)

            section_image = upper_region[top:bottom, left:right]
            output_path = os.path.join(output_folder, f"face_{i+1}_{j+1}_{os.path.basename(image_path)}")
            cv2.imwrite(output_path, section_image)



def crop_dialogs(image_path, output_folder):
    """Crops the image by specified amounts and then divides it into 6 dialog sections.

    Args:
        image_path (str): Path to the input image.
        output_folder (str): Path to the folder where cropped images will be saved.
        crop_left (int, optional): Amount to crop from the left. Defaults to 0.
        crop_right (int, optional): Amount to crop from the right. Defaults to 0.
        crop_top (int, optional): Amount to crop from the top. Defaults to 0.
        crop_bottom (int, optional): Amount to crop from the bottom. Defaults to 0.
    """
    # Adjust these values as needed
    crop_left = 60  
    crop_right = 60 
    crop_top = 0
    crop_bottom = 0 

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at {image_path}")
        return

    height, width, _ = image.shape

    # Crop the image first
    cropped_image = image[crop_top:height - crop_bottom, crop_left:width - crop_right]
    
    # Now work with the cropped image
    height, width, _ = cropped_image.shape 
    dialog_height = height // 2  
    dialog_region = cropped_image[height - dialog_height:, :]

    dialog_width = width // 3

    for i in range(3):
        for j in range(2):
            left = i * dialog_width
            top = j * (dialog_height // 3) 
            right = left + dialog_width
            bottom = top + (dialog_height // 3)

            dialog_image = dialog_region[top:bottom, left:right]
            output_path = os.path.join(output_folder, f"dialog_{i+1}_{j+1}_{os.path.basename(image_path)}")
            cv2.imwrite(output_path, dialog_image)



# Tesseract path configuration
pytesseract.pytesseract.tesseract_cmd = r'D:\OCR_Tesseract\tesseract.exe'

# Specify the folder containing images
folder_path = "Al Hawdaj of the Campus Caravan 1958_Labelled"
destination_folder = "Al Hawdaj of the Campus Caravan 1958_temp" 

# Check if the destination folder exists, if not, create it
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Get all image files in the specified folder (adjust the pattern to match your image types)
image_paths = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))  # Sort by filename

csv_file = 'faces_data.csv'
try:
    df = pd.read_csv(csv_file)
except (pd.errors.EmptyDataError, FileNotFoundError):
    df = pd.DataFrame(columns=['name', 'face_encoding'])

for image_path in image_paths:
    print(image_path)
    
    # Crop and save faces
    crop_upper_sections(image_path, destination_folder)
    # Crop and save dialogs
    crop_dialogs(image_path, destination_folder)

    for i in range(3):
        for j in range(2):
            image_path_dia = os.path.join(destination_folder, f"dialog_{i+1}_{j+1}_{os.path.basename(image_path)}")
            image_path_face = os.path.join(destination_folder, f"face_{i+1}_{j+1}_{os.path.basename(image_path)}")
            
            # Load the image
            image_dia = cv2.imread(image_path_dia)
            image_face = cv2.imread(image_path_face)
            
            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(image_dia)
            
            # Find names preceded by "Mr.", "Mrs.", or "Dr."
            title_names = re.findall(r"(Mr\.|Mrs\.|Dr\.)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text)
            
            # Flatten the list of tuples and remove titles
            names_without_titles = [name for title, name in title_names]
            
            # Find all names in capital letters
            capital_names = re.findall(r"([A-Z]{2,}+[’']?(?:\s|-)[A-Z\'-]{2,}+(?:\s+[A-Z]+)?)\s?", text)
            
            # Combine the two lists of names, removing any duplicates
            all_names = list(dict.fromkeys(capital_names + names_without_titles))
            
            # --- Face Recognition ---
            rgb_image = cv2.cvtColor(image_face, cv2.COLOR_BGR2RGB)
            
            # Find all the faces in the image
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            if len(all_names) == len(face_locations):
                # Create a DataFrame with all names and corresponding face encodings
                new_entries = pd.DataFrame({
                    "name": all_names,
                    "face_encoding": [encoding.tolist() for encoding in face_encodings]
                })
                df = pd.concat([df, new_entries], ignore_index=True)

            try:
                os.remove(image_path_dia)
                os.remove(image_path_face)
            except OSError as e:
                print(f"Error deleting image: {e}")

# Remove the folder (only works if the folder is empty)
os.rmdir(destination_folder)
df.to_csv(csv_file, index=False)