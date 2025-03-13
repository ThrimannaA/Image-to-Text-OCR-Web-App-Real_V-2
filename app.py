# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time

# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  # Load saved credentials 

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  # Authenticate manually
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  # Use existing credentials

# gauth.SaveCredentialsFile("mycreds.txt")  # Save credentials
# drive = GoogleDrive(gauth)

# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Binarization
#     return Image.fromarray(thresh)

# # OCR Functions
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)

# def upload_to_drive(text, ref_number, uploaded_file, errors, rating):
#     """
#     Uploads extracted text, errors, and rating along with the uploaded image 
#     to a newly created folder named after the reference number in Google Drive.
#     """

#     # Define Google Drive Parent Folder ID
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     # Step 1: Check if the folder exists
#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  # Use existing folder
#     else:
#         # Step 2: Create a new folder with the reference number
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Step 3: Save Extracted Text as .txt and Upload
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()
    
#     # Release the file before deleting
#     text_file_drive = None  
#     time.sleep(1)  # Ensure the file is not locked

#     try:
#         os.remove(text_file_path)  # Delete local file
#     except PermissionError:
#         print(f"Retrying deletion of {text_file_path}...")
#         time.sleep(2)
#         try:
#             os.remove(text_file_path)
#         except Exception as e:
#             print(f"Final error deleting {text_file_path}: {e}")

#     # Step 4: Save Errors as .txt and Upload
#     error_file_path = f"{ref_number}_errors.txt"
#     with open(error_file_path, "w", encoding="utf-8") as file:
#         file.write(errors)

#     error_file_drive = drive.CreateFile({'title': f"{ref_number}_errors.txt", 'parents': [{'id': folder_id}]})
#     error_file_drive.SetContentFile(error_file_path)
#     error_file_drive.Upload()

#     error_file_drive = None  # Release the file before deleting
#     time.sleep(1)

#     try:
#         os.remove(error_file_path)  # Delete local file
#     except PermissionError:
#         print(f"Retrying deletion of {error_file_path}...")
#         time.sleep(2)
#         try:
#             os.remove(error_file_path)
#         except Exception as e:
#             print(f"Final error deleting {error_file_path}: {e}")

#     # Step 5: Save and Upload the Uploaded Image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     image_file_drive = None  # Release the file before deleting
#     time.sleep(1)

#     try:
#         os.remove(image_file_path)  # Delete local image file
#     except PermissionError:
#         print(f"Retrying deletion of {image_file_path}...")
#         time.sleep(2)
#         try:
#             os.remove(image_file_path)
#         except Exception as e:
#             print(f"Final error deleting {image_file_path}: {e}")

#     # Step 6: Save Rating as .txt and Upload
#     rating_file_path = f"{ref_number}_rating.txt"
#     with open(rating_file_path, "w", encoding="utf-8") as file:
#         file.write(f"User Rating: {rating}/5")

#     rating_file_drive = drive.CreateFile({'title': f"{ref_number}_rating.txt", 'parents': [{'id': folder_id}]})
#     rating_file_drive.SetContentFile(rating_file_path)
#     rating_file_drive.Upload()

#     rating_file_drive = None  # Release the file before deleting
#     time.sleep(1)

#     try:
#         os.remove(rating_file_path)  # Delete local file
#     except PermissionError:
#         print(f"Retrying deletion of {rating_file_path}...")
#         time.sleep(2)
#         try:
#             os.remove(rating_file_path)
#         except Exception as e:
#             print(f"Final error deleting {rating_file_path}: {e}")

#     return f"✅ Uploaded to Google Drive successfully!"
#     #st.success("✅ Uploaded to Google Drive successfully!")
#     time.sleep(2)
#     st.experimental_rerun()

# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 Let's Extract Text from Images - Instantly! </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)  

#     # Get image height 
#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     # Create two columns for layout
#     col1, col2 = st.columns(2)

#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # New text input area for pasting errors
# errors_text = st.text_area("Paste Any Errors Here", height=200)

# # Rating Selection (1 to 5)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True)

# # Small text input field for Reference Number
# col1, col2 = st.columns([1, 3])  # Adjust the ratio to control width
# with col1:
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)


# # Save & Upload to Google Drive
# if ref_number and st.button("Submit"):
#     message = upload_to_drive(
#         st.session_state["extracted_text"], ref_number, uploaded_file, errors_text, rating
#     )
#     st.success(message)








# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time

# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  # Load saved credentials 

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  # Authenticate manually
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  # Use existing credentials

# gauth.SaveCredentialsFile("mycreds.txt")  # Save credentials
# drive = GoogleDrive(gauth)

# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Binarization
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)


# def upload_to_drive(text, ref_number, uploaded_file, errors, rating):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     def safe_delete(file_path):
#         """Tries to delete a file safely by closing processes and retrying."""
#         for _ in range(3):  # Retry up to 3 times
#             try:
#                 os.remove(file_path)
#                 return  # Exit loop if successful
#             except PermissionError:
#                 time.sleep(1)  # Wait before retrying
#         print(f"Failed to delete {file_path} after multiple attempts.")

#     # **Upload Extracted Text**
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)
#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()
#     text_file_drive = None  # Release file
#     time.sleep(1)  # Ensure file is released
#     safe_delete(text_file_path)  # Try deleting safely

#     # **Upload Errors**
#     error_file_path = f"{ref_number}_errors.txt"
#     with open(error_file_path, "w", encoding="utf-8") as file:
#         file.write(errors)
#     error_file_drive = drive.CreateFile({'title': f"{ref_number}_errors.txt", 'parents': [{'id': folder_id}]})
#     error_file_drive.SetContentFile(error_file_path)
#     error_file_drive.Upload()
#     error_file_drive = None  # Release file
#     time.sleep(1)
#     safe_delete(error_file_path)

#     # **Upload Image**
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()
#     image_file_drive = None  # Release file
#     time.sleep(1)
#     safe_delete(image_file_path)

#     # **Upload Rating**
#     rating_file_path = f"{ref_number}_rating.txt"
#     with open(rating_file_path, "w", encoding="utf-8") as file:
#         file.write(f"User Rating: {rating}/5")
#     rating_file_drive = drive.CreateFile({'title': f"{ref_number}_rating.txt", 'parents': [{'id': folder_id}]})
#     rating_file_drive.SetContentFile(rating_file_path)
#     rating_file_drive.Upload()
#     rating_file_drive = None  # Release file
#     time.sleep(1)
#     safe_delete(rating_file_path)

#     # **Refresh app after upload**
#     st.rerun()

# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 Let's Extract Text from Images - Instantly! </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     # Get image height for text area
#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200)

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True)

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)

# # **Disable Button if Required Fields are Empty**
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True)
# else:
#     if st.button("Submit"):
#         upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file, errors_text, rating)
        
#         # Clear session state values and refresh
#         st.session_state.clear()  # Clears session data after upload
#         # **Refresh app after upload**
#         st.rerun()











# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# import webbrowser 

# # Function to reload the app by refreshing the browser
# def reload_app():
#     st.experimental_set_query_params(refresh="true")  # Set a query param to refresh the page
#     time.sleep(1)  # Give time for the UI to process
#     webbrowser.open(st.experimental_get_query_params())  # Open the same URL


# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # Authenticate Google Sheets
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets
# def upload_to_google_sheets(ref_number, rating, errors):
#     try:
#         client = authenticate_google_sheets()
#         sheet = client.open("OCR_Extraction_Records").sheet1  
#         sheet.append_row([ref_number, rating, errors])  
#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")  

# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)

# # Delete files safely
# def safe_delete(file_path):
#     """Tries to delete a file safely by closing processes and retrying."""
#     for _ in range(3):  
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return  
#         except PermissionError:
#             time.sleep(1)  

# # Upload Extracted Text & Image to Google Drive
# # def upload_to_drive(text, ref_number, uploaded_file):
# #     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

# #     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
# #     folder_list = drive.ListFile({'q': folder_query}).GetList()

# #     if folder_list:
# #         folder_id = folder_list[0]['id']  
# #     else:
# #         folder_metadata = {
# #             'title': ref_number,
# #             'mimeType': 'application/vnd.google-apps.folder',
# #             'parents': [{'id': parent_folder_id}]
# #         }
# #         folder = drive.CreateFile(folder_metadata)
# #         folder.Upload()
# #         folder_id = folder['id']

# #     # Upload Extracted Text
# #     text_file_path = f"{ref_number}_extracted_text.txt"
# #     with open(text_file_path, "w", encoding="utf-8") as file:
# #         file.write(text)
# #     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
# #     text_file_drive.SetContentFile(text_file_path)
# #     text_file_drive.Upload()
# #     #safe_delete(text_file_path)  # Delete after upload

# #     # Delete the text file after successful upload
# #     time.sleep(1)  # Add a small delay to ensure the file is completely released
# #     if os.path.exists(text_file_path):
# #         try:
# #             os.remove(text_file_path)
# #         except PermissionError:
# #             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")

# #     # Upload Image
# #     image_file_path = f"{ref_number}.png"
# #     # Save the uploaded image and ensure it is closed before deleting
# #     image_file_path = f"{ref_number}.png"
# #     img = Image.open(uploaded_file)
# #     img.save(image_file_path)  # Save image to file
# #     img.close()  # Close the image file before deleting

# #     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
# #     image_file_drive.SetContentFile(image_file_path)
# #     image_file_drive.Upload()

# #     #safe_delete(image_file_path)  # Delete after upload

# #     # Delete the image file after successful upload
# #     if os.path.exists(image_file_path):
# #         os.remove(image_file_path)

# #     # Refresh app after upload
# #     st.rerun()

# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Upload Extracted Text
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # Ensure the file is released before deleting
#     text_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(text_file_path):
#         try:
#             os.remove(text_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")

#     # Upload Image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())  # Save the uploaded file

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # Ensure the file is released before deleting
#     image_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(image_file_path):
#         try:
#             os.remove(image_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {image_file_path}. It may still be in use.")

#     # Refresh app after upload
#     st.rerun()

# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Initialize session state values for form fields
# if "rating" not in st.session_state:
#     st.session_state["rating"] = None
# if "ref_number" not in st.session_state:
#     st.session_state["ref_number"] = ""
# if "errors_text" not in st.session_state:
#     st.session_state["errors_text"] = ""

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200, key="errors_text")

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True, key="rating")

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     # ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")
#     ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")

#     if ref_number and not ref_number.isdigit():
#         #st.error("❌ Reference Number must contain only numbers!")
#         ref_number = ""  # Reset invalid input

# # Disable Button if Required Fields are Empty
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True)
# else:
#     if st.button("Submit"):
#         upload_to_google_sheets(ref_number, rating, errors_text)  # Upload errors & rating to Google Sheets
#         upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  # Upload text & image to Drive

#         # Reset session state values before rerunning
#         st.session_state["rating"] = None
#         st.session_state["ref_number"] = ""
#         st.session_state["errors_text"] = ""

#         #st.rerun()  # Refresh app after upload
#         reload_app()







# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# import webbrowser

# # Function to reload the app by refreshing the browser
# def reload_app():
#     st.query_params = {"refresh": "true"}  # Set the query param to refresh the page
#     time.sleep(1)  # Give time for the UI to process

#     # Construct the URL
#     # url = "http://localhost:8505?" + "&".join([f"{k}={v}" for k, v in st.query_params.items()])

#     url = "http://localhost:8505"
#     webbrowser.open(url, new=0) 

#     #Open the URL in the browser
#     #webbrowser.open(url)

#     # Trigger the rerun of the app
#     st.rerun()

# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # Authenticate Google Sheets
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets
# def upload_to_google_sheets(ref_number, rating, errors, timestamp):
#     try:
#         client = authenticate_google_sheets()
        
#         # Format the sheet name with the current date
#         new_sheet_title = f"OCR_Extraction_Records_{timestamp.split(' ')[0]}"  # Only the date part

#         # Try to open the sheet with the formatted name
#         try:
#             sheet = client.open(new_sheet_title).sheet1
#             print(f"Accessing existing sheet: {new_sheet_title}")  # Print when accessing existing sheet
            
#             # Print the sheet URL to the console
#             print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{sheet.id}")

#         except gspread.exceptions.SpreadsheetNotFound:
#             # If sheet doesn't exist, create a new one
#             print(f"Sheet not found, creating new sheet: {new_sheet_title}")  # Print when creating a new sheet
#             sheet = client.create(new_sheet_title).sheet1  # Create a new sheet and get the first sheet
            
#             # Wait for the sheet to be fully created
#             time.sleep(3)  # Add a small delay to allow the sheet to become available
            
#             # Print the sheet URL to the console after creation
#             print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{sheet.id}")

#         # Append the data to the sheet
#         sheet.append_row([timestamp, ref_number, rating, errors])
        
#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")


# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)

# # Delete files safely
# def safe_delete(file_path):
#     """Tries to delete a file safely by closing processes and retrying."""
#     for _ in range(3):  
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return  
#         except PermissionError:
#             time.sleep(1)  

# # Upload Extracted Text & Image to Google Drive
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Upload Extracted Text
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     # Create the text file on Google Drive
#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # Ensure the file is released before deleting
#     text_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(text_file_path):
#         try:
#             os.remove(text_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")
    
#     # Upload Image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())  # Save the uploaded file

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # Ensure the file is released before deleting
#     image_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(image_file_path):
#         try:
#             os.remove(image_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {image_file_path}. It may still be in use.")

#     # Refresh app after upload
#     reload_app()  # Trigger the refresh by rerunning the app


# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Initialize session state values for form fields
# if "rating" not in st.session_state:
#     st.session_state["rating"] = None
# if "ref_number" not in st.session_state:
#     st.session_state["ref_number"] = ""
# if "errors_text" not in st.session_state:
#     st.session_state["errors_text"] = ""

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200, key="errors_text")

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True, key="rating")

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")

#     if ref_number and not ref_number.isdigit():
#         ref_number = ""  # Reset invalid input

# # Disable Button if Required Fields are Empty
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True)
# else:
#     if st.button("Submit"):
#         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Create a timestamp for the current time
#         upload_to_google_sheets(ref_number, rating, errors_text, timestamp)  # Upload to Google Sheets with timestamp
#         upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  # Upload text & image to Drive

#         # Reset session state values before rerunning
#         st.session_state["rating"] = None
#         st.session_state["ref_number"] = ""
#         st.session_state["errors_text"] = ""

#         reload_app()  # Trigger the refresh by rerunning the app






# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  # Load saved credentials 

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  # Authenticate manually
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  # Use existing credentials

# gauth.SaveCredentialsFile("mycreds.txt")  # Save credentials
# drive = GoogleDrive(gauth)

# #Authenticate Google Sheets
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Function to Upload Errors & Rating to Google Sheets
# def upload_to_google_sheets(ref_number, rating, errors):
#     try:
#         client = authenticate_google_sheets()
#         sheet = client.open("OCR_Extraction_Records").sheet1  
#         sheet.append_row([ref_number, rating, errors])  
#         #st.success("✅ Data successfully uploaded to Google Sheets!")
#     except Exception as e:
#         # Remove the error message to suppress it, but you can log it if needed
#         print(f"Error uploading to Google Sheets: {str(e)}")
        
# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Binarization
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)


# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     def safe_delete(file_path):
#         """Tries to delete a file safely by closing processes and retrying."""
#         for _ in range(3):  # Retry up to 3 times
#             try:
#                 os.remove(file_path)
#                 return  # Exit loop if successful
#             except PermissionError:
#                 time.sleep(1)  # Wait before retrying
#         print(f"Failed to delete {file_path} after multiple attempts.")

#     # **Upload Extracted Text**
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)
#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()
#     text_file_drive = None  # Release file
#     time.sleep(1)  # Ensure file is released
#     safe_delete(text_file_path)  # Try deleting safely

#     # # **Upload Errors**
#     # error_file_path = f"{ref_number}_errors.txt"
#     # with open(error_file_path, "w", encoding="utf-8") as file:
#     #     file.write(errors)
#     # error_file_drive = drive.CreateFile({'title': f"{ref_number}_errors.txt", 'parents': [{'id': folder_id}]})
#     # error_file_drive.SetContentFile(error_file_path)
#     # error_file_drive.Upload()
#     # error_file_drive = None  # Release file
#     # time.sleep(1)
#     # safe_delete(error_file_path)

#     # **Upload Image**
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()
#     image_file_drive = None  # Release file
#     time.sleep(1)
#     safe_delete(image_file_path)

#     # # **Upload Rating**
#     # rating_file_path = f"{ref_number}_rating.txt"
#     # with open(rating_file_path, "w", encoding="utf-8") as file:
#     #     file.write(f"User Rating: {rating}/5")
#     # rating_file_drive = drive.CreateFile({'title': f"{ref_number}_rating.txt", 'parents': [{'id': folder_id}]})
#     # rating_file_drive.SetContentFile(rating_file_path)
#     # rating_file_drive.Upload()
#     # rating_file_drive = None  # Release file
#     # time.sleep(1)
#     # safe_delete(rating_file_path)

#     # **Refresh app after upload**
#     st.rerun()

# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 Let's Extract Text from Images - Instantly! </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     # Get image height for text area
#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200)

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True)

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)


# # **Disable Button if Required Fields are Empty**
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True)
# else:
#     if st.button("Submit"):
#         upload_to_google_sheets(ref_number, rating, errors_text)  # Upload errors & rating to Google Sheets
#         upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  # Upload text & image to Drive

#         # Clear session state values and refresh
#         st.session_state.clear()  # Clears session data after upload
#         st.rerun()  # Refresh app after upload





# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# import webbrowser 
# from datetime import datetime

# # Function to reload the app by refreshing the browser
# def reload_app():
#     st.experimental_set_query_params(refresh="true")  # Set a query param to refresh the page
#     time.sleep(1)  # Give time for the UI to process
#     webbrowser.open(st.experimental_get_query_params())  # Open the same URL


# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # Authenticate Google Sheets
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets
# def upload_to_google_sheets(ref_number, rating, errors):
#     try:
#         client = authenticate_google_sheets()
#         sheet = client.open("OCR_Extraction_Records").sheet1  
#         sheet.append_row([ref_number, rating, errors])  
#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")  

# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)

# # Delete files safely
# def safe_delete(file_path):
#     """Tries to delete a file safely by closing processes and retrying."""
#     for _ in range(3):  
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return  
#         except PermissionError:
#             time.sleep(1)  

# # Upload Extracted Text & Image to Google Drive
# # def upload_to_drive(text, ref_number, uploaded_file):
# #     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

# #     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
# #     folder_list = drive.ListFile({'q': folder_query}).GetList()

# #     if folder_list:
# #         folder_id = folder_list[0]['id']  
# #     else:
# #         folder_metadata = {
# #             'title': ref_number,
# #             'mimeType': 'application/vnd.google-apps.folder',
# #             'parents': [{'id': parent_folder_id}]
# #         }
# #         folder = drive.CreateFile(folder_metadata)
# #         folder.Upload()
# #         folder_id = folder['id']

# #     # Upload Extracted Text
# #     text_file_path = f"{ref_number}_extracted_text.txt"
# #     with open(text_file_path, "w", encoding="utf-8") as file:
# #         file.write(text)
# #     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
# #     text_file_drive.SetContentFile(text_file_path)
# #     text_file_drive.Upload()
# #     #safe_delete(text_file_path)  # Delete after upload

# #     # Delete the text file after successful upload
# #     time.sleep(1)  # Add a small delay to ensure the file is completely released
# #     if os.path.exists(text_file_path):
# #         try:
# #             os.remove(text_file_path)
# #         except PermissionError:
# #             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")

# #     # Upload Image
# #     image_file_path = f"{ref_number}.png"
# #     # Save the uploaded image and ensure it is closed before deleting
# #     image_file_path = f"{ref_number}.png"
# #     img = Image.open(uploaded_file)
# #     img.save(image_file_path)  # Save image to file
# #     img.close()  # Close the image file before deleting

# #     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
# #     image_file_drive.SetContentFile(image_file_path)
# #     image_file_drive.Upload()

# #     #safe_delete(image_file_path)  # Delete after upload

# #     # Delete the image file after successful upload
# #     if os.path.exists(image_file_path):
# #         os.remove(image_file_path)

# #     # Refresh app after upload
# #     st.rerun()

# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Upload Extracted Text
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # Ensure the file is released before deleting
#     text_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(text_file_path):
#         try:
#             os.remove(text_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")

#     # Upload Image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())  # Save the uploaded file

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # Ensure the file is released before deleting
#     image_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(image_file_path):
#         try:
#             os.remove(image_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {image_file_path}. It may still be in use.")

#     # Refresh app after upload
#     st.rerun()

# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Initialize session state values for form fields
# if "rating" not in st.session_state:
#     st.session_state["rating"] = None
# if "ref_number" not in st.session_state:
#     st.session_state["ref_number"] = ""
# if "errors_text" not in st.session_state:
#     st.session_state["errors_text"] = ""

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200, key="errors_text")

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[1, 2, 3, 4, 5], horizontal=True, key="rating")

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     # ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")
#     ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")

#     if ref_number and not ref_number.isdigit():
#         #st.error("❌ Reference Number must contain only numbers!")
#         ref_number = ""  # Reset invalid input

# # Disable Button if Required Fields are Empty
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True)
# else:
#     if st.button("Submit"):
#         upload_to_google_sheets(ref_number, rating, errors_text)  # Upload errors & rating to Google Sheets
#         upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  # Upload text & image to Drive

#         # Reset session state values before rerunning
#         st.session_state["rating"] = None
#         st.session_state["ref_number"] = ""
#         st.session_state["errors_text"] = ""

#         #st.rerun()  # Refresh app after upload
#         reload_app()






# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# import webbrowser 
# from datetime import datetime

# # Function to reload the app by refreshing the browser
# def reload_app():
#     st.query_params = {"refresh": "true"}  # Set the query param to refresh the page
#     time.sleep(1)  # Give time for the UI to process

#     # Construct the URL
#     # url = "http://localhost:8507?" + "&".join([f"{k}={v}" for k, v in st.query_params.items()])

#     url = "http://localhost:8506"
#     webbrowser.open(url, new=0) 

#     #Open the URL in the browser
#     # webbrowser.open(url)

#     # Trigger the rerun of the app
#     st.rerun()

# st.set_page_config(layout="wide")  # Enables wide mode

# # Initialize Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # Authenticate Google Sheets
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# from datetime import datetime

# # Upload to Google Sheets with Dynamic Sheet Naming
# def upload_to_google_sheets(ref_number, rating, errors):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")  

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date already exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="5")

#             # Add headers to the new sheet
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors"])

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append the new data
#         sheet.append_row([time_str, ref_number, rating, errors])  

#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")  


# # Preprocess Image for OCR
# def preprocess_image(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  
#     return Image.fromarray(thresh)

# # OCR Function
# def extract_text_tesseract(image):
#     return pytesseract.image_to_string(image)

# # Delete files safely
# def safe_delete(file_path):
#     """Tries to delete a file safely by closing processes and retrying."""
#     for _ in range(3):  
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return  
#         except PermissionError:
#             time.sleep(1)  


# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']  
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Upload Extracted Text
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # Ensure the file is released before deleting
#     text_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(text_file_path):
#         try:
#             os.remove(text_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {text_file_path}. It may still be in use.")

#     # Upload Image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())  # Save the uploaded file

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # Ensure the file is released before deleting
#     image_file_drive = None  # Remove reference to Drive file
#     gc.collect()  # Force garbage collection

#     time.sleep(2)  # Wait before attempting to delete

#     if os.path.exists(image_file_path):
#         try:
#             os.remove(image_file_path)
#         except PermissionError:
#             print(f"Warning: Unable to delete {image_file_path}. It may still be in use.")

#     # Refresh app after upload
#     # st.rerun()
#     reload_app()


# # Streamlit UI
# st.markdown(
#     "<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#     unsafe_allow_html=True
# )

# uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     img = Image.open(uploaded_file)
#     preprocessed_img = preprocess_image(img)
#     extracted_text = extract_text_tesseract(preprocessed_img)

#     img_width, img_height = img.size
#     text_area_height = min(img_height, 800)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#     with col2:
#         st.text_area("Extracted Text", extracted_text, height=text_area_height)

#     st.session_state["extracted_text"] = extracted_text

# # Initialize session state values for form fields
# if "rating" not in st.session_state:
#     st.session_state["rating"] = None
# if "ref_number" not in st.session_state:
#     st.session_state["ref_number"] = ""
# if "errors_text" not in st.session_state:
#     st.session_state["errors_text"] = ""

# # Text area for errors
# errors_text = st.text_area("Paste Any Errors Here", height=200, key="errors_text")

# # Rating Selection (Mandatory)
# rating = st.radio("Rate the OCR Extraction (1-5)", options=[5, 4, 3, 2, 1], horizontal=True, key="rating")

# # Reference Number Input
# col1, col2 = st.columns([1, 3])
# with col1:
#     # ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")
#     ref_number = st.text_input("Enter Reference Number", max_chars=10, key="ref_number")

#     if ref_number and not ref_number.isdigit():
#         #st.error("❌ Reference Number must contain only numbers!")
#         ref_number = ""  # Reset invalid input

# # Disable Button if Required Fields are Empty
# if not ref_number or rating is None:
#     st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#     st.button("Save & Upload to Google Drive", disabled=True, key="disabled_button")
# else:
#     if st.button("Submit", key="submit_button"):
#         try:
#             # Perform both uploads
#             upload_to_google_sheets(ref_number, rating, errors_text)  
#             upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  

#             # Show success message in UI
#             success_message = st.empty()  # Create an empty container for dynamic updates
#             success_message.success("✅ Saved successfully!")

#             # Wait for 3 seconds so the user can see the success message
#             time.sleep(3)

#             # Clear success message before reloading
#             success_message.empty()

#             # Reset session state values before rerunning
#             st.session_state["rating"] = None
#             st.session_state["ref_number"] = ""
#             st.session_state["errors_text"] = ""

#             # Refresh app after successful upload
#             st.rerun()  # Use `st.rerun()` instead of `reload_app()`

#         except Exception as e:
#             # Show error message if upload fails
#             st.error(f"❌ Upload failed: {str(e)}")







# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# from datetime import datetime

# # Set Page Config (Must be first!)
# st.set_page_config(layout="wide")  

# # Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # **Authenticate Google Sheets**
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets with Dynamic Sheet Naming
# def upload_to_google_sheets(ref_number, rating, errors, selected_user):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")  

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date already exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="6")  # 6 columns (added User column)

#             # Add headers to the new sheet
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors", "User"])  # Added "User" column

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append the new data including selected_user
#         sheet.append_row([time_str, ref_number, rating, errors, selected_user])  # Append selected_user

#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")


# # **Google Drive Upload Function**
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     text_file_path = f"{ref_number}_extracted_text.txt"
    
#     # ✅ Write and Close the File Properly
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     # ✅ Wait before accessing the file
#     time.sleep(1)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # ✅ Ensure File is Released Before Deleting
#     del text_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(text_file_path):
#         os.remove(text_file_path)

#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # ✅ Ensure Image File is Released Before Deleting
#     del image_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(image_file_path):
#         os.remove(image_file_path)

# # **User Selection State**
# if "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = False
# if "selected_user" not in st.session_state:
#     st.session_state["selected_user"] = None

# # Function to reset user selection
# def reset_user_selection():
#     st.session_state["user_selected"] = False
#     st.session_state["selected_user"] = None
#     st.rerun()

# # **User Selection Page** (Only appears when no user is selected)
# if not st.session_state["user_selected"]:
#     st.title("Select Your Name")

#     user_names = ["Alice", "Bob", "Charlie", "David"]  # Replace with actual names
#     selected_user = st.selectbox("Choose your name:", user_names)

#     if st.button("Continue"):
#         st.session_state["user_selected"] = True
#         st.session_state["selected_user"] = selected_user
#         st.rerun()  # Refresh to load main UI

# # **Main UI (Only loads after user selection)**
# if st.session_state["user_selected"]:
#     st.sidebar.button("🔄 Change User", on_click=reset_user_selection)  

#     st.markdown(
#         f"<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#         unsafe_allow_html=True
#     )

#     uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

#     if uploaded_file:
#         img = Image.open(uploaded_file)
#         preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#         extracted_text = pytesseract.image_to_string(preprocessed_img)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#         with col2:
#             st.text_area("Extracted Text", extracted_text, height=500)

#         st.session_state["extracted_text"] = extracted_text

#     # Input Fields
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)
#     rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)
#     errors_text = st.text_area("Paste Any Errors Here", height=200)

#     if not ref_number or rating is None:
#         st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#         st.button("Submit", disabled=True)
#     else:
#         if st.button("Submit"):
#             try:
#                 # ✅ Upload extracted text & image to Google Drive
#                 upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  

#                 # ✅ Upload details to Google Sheets
#                 upload_to_google_sheets(ref_number, rating, errors_text, st.session_state["selected_user"])  

#                 st.success("✅ Saved successfully!")
                
#                 # ✅ Clear session state and refresh the page
#                 time.sleep(2)  # Small delay for user to see success message
#                 st.session_state.clear()  # Reset all stored values
#                 st.rerun()  # Refresh the page

#             except Exception as e:
#                 st.error(f"❌ Upload failed: {str(e)}")








# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# from datetime import datetime

# # Set Page Config (Must be first!)
# st.set_page_config(layout="wide")  

# # Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # **Authenticate Google Sheets**
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets with Dynamic Sheet Naming
# def upload_to_google_sheets(ref_number, rating, errors, selected_user):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")  

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date already exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="6")  # 6 columns (added User column)

#             # Add headers to the new sheet
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors", "User"])  # Added "User" column

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append the new data including selected_user
#         sheet.append_row([time_str, ref_number, rating, errors, selected_user])  # Append selected_user

#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")


# # **Google Drive Upload Function**
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     text_file_path = f"{ref_number}_extracted_text.txt"
    
#     # ✅ Write and Close the File Properly
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     # ✅ Wait before accessing the file
#     time.sleep(1)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # ✅ Ensure File is Released Before Deleting
#     del text_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(text_file_path):
#         os.remove(text_file_path)

#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # ✅ Ensure Image File is Released Before Deleting
#     del image_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(image_file_path):
#         os.remove(image_file_path)

# # **User Selection State**
# if "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = False
# if "selected_user" not in st.session_state:
#     st.session_state["selected_user"] = None

# # Function to reset user selection
# def reset_user_selection():
#     st.session_state["user_selected"] = False
#     st.session_state["selected_user"] = None
#     st.rerun()

# # **User Selection Page** (Only appears when no user is selected)
# if not st.session_state["user_selected"]:
#     st.title("Select Your Name")

#     user_names = ["Alice", "Bob", "Charlie", "David"]  # Replace with actual names
#     selected_user = st.selectbox("Choose your name:", user_names)

#     if st.button("Continue"):
#         st.session_state["user_selected"] = True
#         st.session_state["selected_user"] = selected_user
#         st.rerun()  # Refresh to load main UI

# # **Main UI (Only loads after user selection)**
# if st.session_state["user_selected"]:
#     st.sidebar.button("🔄 Change User", on_click=reset_user_selection)  

#     st.markdown(
#         f"<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#         unsafe_allow_html=True
#     )

#     uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

#     if uploaded_file:
#         img = Image.open(uploaded_file)
#         preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#         extracted_text = pytesseract.image_to_string(preprocessed_img)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#         with col2:
#             st.text_area("Extracted Text", extracted_text, height=500)

#         st.session_state["extracted_text"] = extracted_text

#     # Input Fields
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)
#     rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)
#     errors_text = st.text_area("Paste Any Errors Here", height=200)

#     if not ref_number or rating is None:
#         st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#         st.button("Submit", disabled=True)
#     else:
#         if st.button("Submit"):
#             try:
#                 # ✅ Upload extracted text & image to Google Drive
#                 upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  

#                 # ✅ Upload details to Google Sheets
#                 upload_to_google_sheets(ref_number, rating, errors_text, st.session_state["selected_user"])  

#                 st.success("✅ Saved successfully!")
                
#                 # ✅ Clear session state and refresh the page
#                 time.sleep(2)  # Small delay for user to see success message
#                 st.session_state.clear()  # Reset all stored values
#                 st.rerun()  # Refresh the page

#             except Exception as e:
#                 st.error(f"❌ Upload failed: {str(e)}")





# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# from datetime import datetime

# # Set Page Config (Must be first!)
# st.set_page_config(layout="wide")  

# # Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # **Authenticate Google Sheets**
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets with Dynamic Sheet Naming
# def upload_to_google_sheets(ref_number, rating, errors, selected_user):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")  

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date already exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="6")  # 6 columns (added User column)

#             # Add headers to the new sheet
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors", "User"])  # Added "User" column

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append the new data including selected_user
#         sheet.append_row([time_str, ref_number, rating, errors, selected_user])  # Append selected_user

#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")


# # **Google Drive Upload Function**
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     text_file_path = f"{ref_number}_extracted_text.txt"
    
#     # ✅ Write and Close the File Properly
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     # ✅ Wait before accessing the file
#     time.sleep(1)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # ✅ Ensure File is Released Before Deleting
#     del text_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(text_file_path):
#         os.remove(text_file_path)

#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # ✅ Ensure Image File is Released Before Deleting
#     del image_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(image_file_path):
#         os.remove(image_file_path)

# # **User Selection State**
# if "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = False
# if "selected_user" not in st.session_state:
#     st.session_state["selected_user"] = None

# # Function to reset user selection
# def reset_user_selection():
#     st.session_state["user_selected"] = False
#     st.session_state["selected_user"] = None
#     st.rerun()

# # **User Selection Page** (Only appears when no user is selected)
# if not st.session_state["user_selected"]:
#     st.title("Select Your Name")

#     user_names = ["Alice", "Bob", "Charlie", "David"]  # Replace with actual names
#     selected_user = st.selectbox("Choose your name:", user_names)

#     if st.button("Continue"):
#         st.session_state["user_selected"] = True
#         st.session_state["selected_user"] = selected_user
#         st.rerun()  # Refresh to load main UI

# # **Main UI (Only loads after user selection)**
# if st.session_state["user_selected"]:
#     st.sidebar.button("🔄 Change User", on_click=reset_user_selection)  

#     st.markdown(
#         f"<h1 style='text-align: center;'>🔍 One Click Extraction of Text from Images </h1>",
#         unsafe_allow_html=True
#     )

#     uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

#     if uploaded_file:
#         img = Image.open(uploaded_file)
#         preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#         extracted_text = pytesseract.image_to_string(preprocessed_img)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#         with col2:
#             st.text_area("Extracted Text", extracted_text, height=500)

#         st.session_state["extracted_text"] = extracted_text

#     # Input Fields
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)
#     rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)
#     errors_text = st.text_area("Paste Any Errors Here", height=200)

#     if not ref_number or rating is None:
#         st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#         st.button("Submit", disabled=True)
#     else:
#         if st.button("Submit"):
#             try:
#                 # ✅ Upload extracted text & image to Google Drive
#                 upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  

#                 # ✅ Upload details to Google Sheets
#                 upload_to_google_sheets(ref_number, rating, errors_text, st.session_state["selected_user"])  

#                 st.success("✅ Saved successfully!")
                
#                 # ✅ Clear session state and refresh the page
#                 time.sleep(2)  # Small delay for user to see success message
#                 st.session_state.clear()  # Reset all stored values
#                 st.rerun()  # Refresh the page

#             except Exception as e:
#                 st.error(f"❌ Upload failed: {str(e)}")




# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# from datetime import datetime

# # Set Page Config (Must be first!)
# st.set_page_config(layout="wide")  

# # Google Drive Authentication
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")  

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()  
# elif gauth.access_token_expired:
#     gauth.Refresh()  
# else:
#     gauth.Authorize()  

# gauth.SaveCredentialsFile("mycreds.txt")  
# drive = GoogleDrive(gauth)

# # **Authenticate Google Sheets**
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client

# # Upload to Google Sheets with Dynamic Sheet Naming
# def upload_to_google_sheets(ref_number, rating, errors, selected_user):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")  

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date already exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="6")  # 6 columns (added User column)

#             # Add headers to the new sheet
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors", "User"])  # Added "User" column

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append the new data including selected_user
#         sheet.append_row([time_str, ref_number, rating, errors, selected_user])  # Append selected_user

#     except Exception as e:
#         print(f"Error uploading to Google Sheets: {str(e)}")


# # **Google Drive Upload Function**
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'  

#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']
#     else:
#         folder_metadata = {
#             'title': ref_number,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [{'id': parent_folder_id}]
#         }
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     text_file_path = f"{ref_number}_extracted_text.txt"
    
#     # ✅ Write and Close the File Properly
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     # ✅ Wait before accessing the file
#     time.sleep(1)

#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()

#     # ✅ Ensure File is Released Before Deleting
#     del text_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(text_file_path):
#         os.remove(text_file_path)

#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()

#     # ✅ Ensure Image File is Released Before Deleting
#     del image_file_drive
#     gc.collect()
#     time.sleep(2)

#     if os.path.exists(image_file_path):
#         os.remove(image_file_path)

# # **User Selection State**
# if "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = False
# if "selected_user" not in st.session_state:
#     st.session_state["selected_user"] = None

# # Function to reset user selection
# def reset_user_selection():
#     st.session_state["user_selected"] = False
#     st.session_state["selected_user"] = None
#     st.rerun()


# # **User Selection Page** (Only appears when no user is selected)
# if not st.session_state["user_selected"]:
#     st.title("👋Let’s Get Started! Identify Yourself to Begin")

#     user_names = ["DS", "NW", "RB", "IG", "AR","NU"]  
#     selected_user = st.selectbox("Choose your name:", user_names, index=None)

#     # Disable "Continue" button if no user is selected
#     continue_button = st.button("Continue", disabled=not selected_user)

#     if continue_button:
#         st.session_state["user_selected"] = True
#         st.session_state["selected_user"] = selected_user
#         st.rerun()  # Refresh to load main UI

#     if not selected_user:
#         st.warning("⚠ Please select a user to continue.")



# # **Main UI (Only loads after user selection)**
# if st.session_state["user_selected"]:

#     st.markdown(
#         f"<h1 style='text-align: center;'>🔍Extract Job Info in One Click </h1>",
#         unsafe_allow_html=True
#     )

#     uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

#     if uploaded_file:
#         img = Image.open(uploaded_file)
#         preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#         extracted_text = pytesseract.image_to_string(preprocessed_img)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
#         # with col2:
#         #     st.text_area("Extracted Text", extracted_text, height=len(extracted_text.split("\n")) * 20, key="extracted_text_display")

        
#         with col2:
#             st.markdown(
#                 f"""
#                 <div style="border: 1px solid #ccc; padding: 10px; width: 100%; white-space: pre-wrap; overflow: hidden; text-align: left;">
#                     {extracted_text}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
        

#         st.session_state["extracted_text"] = extracted_text

#     # Input Fields
#     errors_text = st.text_area("Paste Any Errors Here", height=200)
#     rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)

#     # Reference number validation: only numbers, no longer than 10 characters
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)
#     if ref_number and not ref_number.isdigit():
#         st.warning("⚠ Reference Number must be a number.")
#         ref_number = ""

#     if not ref_number or rating is None:
#         st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#         st.button("Submit", disabled=True)
#     else:
#         if st.button("Submit"):
#             try:
#                 # ✅ Upload extracted text & image to Google Drive
#                 upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)  

#                 # ✅ Upload details to Google Sheets
#                 upload_to_google_sheets(ref_number, st.session_state["selected_user"],rating, errors_text)  

#                 st.success("✅ Saved successfully!")
                
#                 # ✅ Clear session state and refresh the page
#                 time.sleep(2)  # Small delay for user to see success message
#                 st.session_state.clear()  # Reset all stored values
#                 st.rerun()  # Refresh the page

#             except Exception as e:
#                 st.error(f"❌ Upload failed: {str(e)}")







# import streamlit as st
# import pytesseract
# from PIL import Image
# import cv2
# import numpy as np
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import gc
# from datetime import datetime

# # Set Page Config (Must be first!)
# st.set_page_config(layout="wide")

# # **Google Drive Authentication**
# gauth = GoogleAuth()
# gauth.LoadCredentialsFile("mycreds.txt")

# if gauth.credentials is None:
#     gauth.LocalWebserverAuth()
# elif gauth.access_token_expired:
#     gauth.Refresh()
# else:
#     gauth.Authorize()

# gauth.SaveCredentialsFile("mycreds.txt")
# drive = GoogleDrive(gauth)


# # **Authenticate Google Sheets**
# def authenticate_google_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)
#     return client


# # **Upload to Google Sheets with Dynamic Sheet Naming**
# def upload_to_google_sheets(ref_number, rating, errors, selected_user):
#     try:
#         client = authenticate_google_sheets()
#         spreadsheet = client.open("OCR_Extraction_Records")

#         # Get the current date in YYYY-MM-DD format
#         today_date = datetime.now().strftime("%Y-%m-%d")

#         # Check if a sheet with today's date exists
#         sheet_list = spreadsheet.worksheets()
#         sheet_names = [sheet.title for sheet in sheet_list]

#         if today_date in sheet_names:
#             sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
#         else:
#             # Create a new sheet with the date
#             sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="5")  # 5 columns

#             # Add headers
#             sheet.append_row(["Time", "Reference Number", "Rating", "Errors", "User"])

#         # Get current time
#         time_str = datetime.now().strftime("%H:%M:%S")

#         # Append new data
#         sheet.append_row([time_str, ref_number, rating, errors, selected_user])

#     except Exception as e:
#         st.error(f"❌ Error uploading to Google Sheets: {str(e)}")


# # **Google Drive Upload Function**
# def upload_to_drive(text, ref_number, uploaded_file):
#     parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'

#     # Check if folder exists
#     folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
#     folder_list = drive.ListFile({'q': folder_query}).GetList()

#     if folder_list:
#         folder_id = folder_list[0]['id']
#     else:
#         folder_metadata = {'title': ref_number, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': parent_folder_id}]}
#         folder = drive.CreateFile(folder_metadata)
#         folder.Upload()
#         folder_id = folder['id']

#     # Upload text file
#     text_file_path = f"{ref_number}_extracted_text.txt"
#     with open(text_file_path, "w", encoding="utf-8") as file:
#         file.write(text)

#     time.sleep(1)
#     text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
#     text_file_drive.SetContentFile(text_file_path)
#     text_file_drive.Upload()
#     del text_file_drive
#     gc.collect()
#     os.remove(text_file_path)

#     # Upload image
#     image_file_path = f"{ref_number}.png"
#     with open(image_file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
#     image_file_drive.SetContentFile(image_file_path)
#     image_file_drive.Upload()
#     del image_file_drive
#     gc.collect()
#     os.remove(image_file_path)


# # **User Selection State**
# if "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = False
# if "selected_user" not in st.session_state:
#     st.session_state["selected_user"] = None


# # **User Selection Page (Only appears when no user is selected)**
# @st.cache_data
# def get_user_names():
#     return ["DS", "NW", "RB", "IG", "AR", "NU"]

# user_names = get_user_names()

# # Retrieve cached user from query params
# query_params = st.query_params
# cached_user = query_params.get("user", None)

# if cached_user and "user_selected" not in st.session_state:
#     st.session_state["user_selected"] = True
#     st.session_state["selected_user"] = cached_user

# if not st.session_state["user_selected"]:
#     st.title("👋 Let’s Get Started! Identify Yourself to Begin")

#     selected_user = st.selectbox("Choose your name:", user_names, index=user_names.index(cached_user) if cached_user in user_names else None)
#     continue_button = st.button("Continue", disabled=not selected_user)

#     if continue_button:
#         st.session_state["user_selected"] = True
#         st.session_state["selected_user"] = selected_user
#         st.query_params["user"] = selected_user
#         st.rerun()

#     if not selected_user:
#         st.warning("⚠ Please select a user to continue.")
# else:
#     st.write(f"✅ Welcome back, {st.session_state['selected_user']}!")


# # **Main UI (Only loads after user selection)**
# if st.session_state["user_selected"]:
#     st.markdown("<h1 style='text-align: center;'>🔍 Extract Job Info in One Click</h1>", unsafe_allow_html=True)

#     uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

#     if uploaded_file:
#         img = Image.open(uploaded_file)
#         preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
#         extracted_text = pytesseract.image_to_string(preprocessed_img)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#         with col2:
#             st.text_area("Extracted Text", extracted_text, height=200, key="extracted_text_display")

#         st.session_state["extracted_text"] = extracted_text

#     errors_text = st.text_area("Paste Any Errors Here", height=200)
#     rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)
#     ref_number = st.text_input("Enter Reference Number", max_chars=10)

#     if ref_number and not ref_number.isdigit():
#         st.warning("⚠ Reference Number must be a number.")
#         ref_number = ""

#     if not ref_number or rating is None:
#         st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
#         st.button("Submit", disabled=True)
#     else:
#         if st.button("Submit"):
#             try:
#                 upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)
#                 upload_to_google_sheets(ref_number, rating, errors_text, st.session_state["selected_user"])
#                 st.success("✅ Saved successfully!")
#                 time.sleep(2)
#                 st.session_state.clear()
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"❌ Upload failed: {str(e)}")





import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gc
from datetime import datetime

# Set Page Config (Must be first!)
st.set_page_config(layout="wide")

# **Google Drive Authentication**
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)


# **Authenticate Google Sheets**
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client


# **Upload to Google Sheets with Dynamic Sheet Naming**
def upload_to_google_sheets(ref_number, rating, errors, selected_user):
    try:
        client = authenticate_google_sheets()
        spreadsheet = client.open("OCR_Extraction_Records")

        # Get the current date in YYYY-MM-DD format
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if a sheet with today's date exists
        sheet_list = spreadsheet.worksheets()
        sheet_names = [sheet.title for sheet in sheet_list]

        if today_date in sheet_names:
            sheet = spreadsheet.worksheet(today_date)  # Use existing sheet
        else:
            # Create a new sheet with the date
            sheet = spreadsheet.add_worksheet(title=today_date, rows="1000", cols="5")  # 5 columns

            # Add headers
            sheet.append_row(["Time", "Reference Number", "User", "Rating", "Error Traces"])

        # Get current time
        time_str = datetime.now().strftime("%H:%M:%S")

        # Append new data
        sheet.append_row([time_str, ref_number, selected_user,rating, errors])

    except Exception as e:
        st.error(f"❌ Error uploading to Google Sheets: {str(e)}")


# **Google Drive Upload Function**
def upload_to_drive(text, ref_number, uploaded_file):
    parent_folder_id = '1SXT8l8R1i3LktVSxU5mosdU5TczIVT_F'

    # Check if folder exists
    folder_query = f"title='{ref_number}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    folder_list = drive.ListFile({'q': folder_query}).GetList()

    if folder_list:
        folder_id = folder_list[0]['id']
    else:
        folder_metadata = {'title': ref_number, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': parent_folder_id}]}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        folder_id = folder['id']

    # Upload text file
    text_file_path = f"{ref_number}_extracted_text.txt"
    with open(text_file_path, "w", encoding="utf-8") as file:
        file.write(text)

    time.sleep(1)
    text_file_drive = drive.CreateFile({'title': f"{ref_number}_extracted_text.txt", 'parents': [{'id': folder_id}]})
    text_file_drive.SetContentFile(text_file_path)
    text_file_drive.Upload()
    del text_file_drive
    gc.collect()
    os.remove(text_file_path)

    # Upload image
    image_file_path = f"{ref_number}.png"
    with open(image_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    image_file_drive = drive.CreateFile({'title': f"{ref_number}.png", 'parents': [{'id': folder_id}]})
    image_file_drive.SetContentFile(image_file_path)
    image_file_drive.Upload()
    del image_file_drive
    gc.collect()
    os.remove(image_file_path)


# **User Selection State**
if "user_selected" not in st.session_state:
    st.session_state["user_selected"] = False
if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = None


# **User Selection Page (Only appears when no user is selected)**
@st.cache_data
def get_user_names():
    return ["DS", "NW", "RB", "IG", "AR", "NU"]

user_names = get_user_names()

# Retrieve cached user from query params
query_params = st.query_params
cached_user = query_params.get("user", None)

if cached_user and "user_selected" not in st.session_state:
    st.session_state["user_selected"] = True
    st.session_state["selected_user"] = cached_user

if not st.session_state["user_selected"]:
    st.title("👋 Let’s Get Started! Identify Yourself to Begin")

    selected_user = st.selectbox("Choose your name:", user_names, index=user_names.index(cached_user) if cached_user in user_names else None)
    continue_button = st.button("Continue", disabled=not selected_user)

    if continue_button:
        st.session_state["user_selected"] = True
        st.session_state["selected_user"] = selected_user
        st.query_params["user"] = selected_user
        st.rerun()

    if not selected_user:
        st.warning("⚠ Please select a user to continue.")
else:
    st.write(f"✅ Welcome Back, {st.session_state['selected_user']}!")


# **Main UI (Only loads after user selection)**
if st.session_state["user_selected"]:
    st.markdown("<h1 style='text-align: center;'>🔍 Extract Job Info in One Click</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        preprocessed_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        extracted_text = pytesseract.image_to_string(preprocessed_img)

        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        # Display extracted text as a single column without scrolling
        with col2:
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; padding: 10px; width: 100%; white-space: pre-wrap; overflow: hidden; text-align: left;">
                    {extracted_text}
                </div>
                """,
                unsafe_allow_html=True
            )


        st.session_state["extracted_text"] = extracted_text

    errors_text = st.text_area("Paste Any Errors Here", height=200)
    rating = st.radio("Rate the OCR Extraction (5-1)", options=[5, 4, 3, 2, 1], index=None, horizontal=True)
    ref_number = st.text_input("Enter Reference Number", max_chars=10)

    if ref_number and not ref_number.isdigit():
        st.warning("⚠ Reference Number must be a number.")
        ref_number = ""

    if not ref_number or rating is None:
        st.warning("⚠ Please enter a Reference Number and select a Rating to proceed.")
        st.button("Submit", disabled=True)
    else:
        if st.button("Submit"):
            try:
                upload_to_drive(st.session_state["extracted_text"], ref_number, uploaded_file)
                upload_to_google_sheets(ref_number, rating, errors_text, st.session_state["selected_user"])
                st.success("✅ Saved successfully!")
                time.sleep(2)
                st.session_state.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Upload failed: {str(e)}")