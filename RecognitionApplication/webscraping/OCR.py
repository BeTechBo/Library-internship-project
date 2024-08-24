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


# First Version Working

# Tesseract path configuration 
pytesseract.pytesseract.tesseract_cmd = r'D:\OCR_Tesseract\tesseract.exe'

# Specify the folder containing images
folder_path = "Al Hawdaj of the Campus Caravan 1958"
destination_folder = "Al Hawdaj of the Campus Caravan 1958_Labelled"  # Define the destination folder

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
    # Load the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: The image at path {image_path} could not be loaded.")
    else:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(image)
    
        # Find names preceded by "Mr.", "Mrs.", or "Dr."
        title_names = re.findall(r"(Mr\.|Mrs\.|Dr\.)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text)
    
        # Flatten the list of tuples and remove titles
        names_without_titles = []
        for title, name in title_names:
          names_without_titles.append(name)
                
        # Find all names in capital letters
        capital_names = re.findall(r"([A-Z]{2,}+[’']?(?:\s|-)[A-Z\'-]{2,}+(?:\s+[A-Z]+)?)\s?", text) #r"([A-Z]{3,}+[’'-]?(?:\s|-)[A-Z\'-]+)\s?" ----------- r'\n([A-Z]+\s[A-Z\'-]+)\s?\.\.\.'
    
        # Combine the two lists of names, removing any duplicates
        all_names = list(dict.fromkeys(capital_names + names_without_titles))
    
        # --- Face Recognition ---
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # Find all the faces in the image
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if len(all_names) == len(face_locations):
            print(all_names)
            print(f"The number of detected names match the number of detected faces in {image_path}.")
            
            # Create a DataFrame with all names and corresponding face encodings
            new_entries = pd.DataFrame({
                "name": all_names,
                "face_encoding": [encoding.tolist() for encoding in face_encodings]
            })
            df = pd.concat([df, new_entries], ignore_index=True)
            
            # Move the image to the destination folder after processing
            shutil.move(image_path, os.path.join(destination_folder, os.path.basename(image_path)))
        else:
            print(f"Warning: The number of detected names does not match the number of detected faces in {image_path}.")

df.to_csv(csv_file, index=False)