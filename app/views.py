from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pytesseract
from PIL import Image
from datetime import datetime
# Create your views here.
from rest_framework.parsers import MultiPartParser,FormParser
import re


from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        # Get the uploaded file
        file_obj = request.FILES.get('image')
        
        # Save the uploaded file
        file_path = default_storage.save(file_obj.name, ContentFile(file_obj.read()))
        
        # Check if the file is a PDF
        if file_path.endswith('.pdf'):
            # Extract images from the PDF
            images = convert_from_path(default_storage.path(file_path))
            
            # Initialize a list to store extracted items
            extracted_items = []
            
            # Total amount
            total_amount = 0.0
            
            # Process each page/image
            for idx, image in enumerate(images):
                # Convert image to text using OCR
                extracted_text = pytesseract.image_to_string(image)
                
                # Extract item details from the OCR result using regular expressions
                item_details = re.findall(r'([A-Z\s]+)\s+(\d+)\s+(\d+\.\d{2})', extracted_text)
                
                # Extracted data for each item
                for item in item_details:
                    name = item[0].strip()
                    quantity = int(item[1])
                    amount = float(item[2])
                    
                    # Add the amount to the total
                    total_amount += amount
                    
                    # You may need to handle date separately if it's not included in the OCR text
                    # For now, I'll leave it as None
                    date = None
                    
                    # Create a dictionary for the item
                    item_data = {
                        "name": name,
                        "quantity": quantity,
                        "date": date,
                        "amount": amount
                    }
                    
                    extracted_items.append(item_data)
            
            # You can now do whatever you want with the extracted items and total amount
            # For demonstration, I'm just returning the extracted items and total amount as a response
            response_data = {
                "items": extracted_items,
                "total_amount": total_amount
            }
            return Response(response_data, status=200)
        
        else:
            # If the file is not a PDF, handle it as an image
            # Perform OCR on the uploaded image
            image = Image.open(default_storage.path(file_path))
            extracted_text = pytesseract.image_to_string(image)
            
            # Extract item details from the OCR result using regular expressions
            item_details = re.findall(r'([A-Z\s]+)\s+(\d+)\s+(\d+\.\d{2})', extracted_text)
            
            # Initialize a list to store extracted items
            extracted_items = []
            
            # Total amount
            total_amount = 0.0
            
            # Extracted data for each item
            for item in item_details:
                name = item[0].strip()
                quantity = int(item[1])
                amount = float(item[2])
                
                # Add the amount to the total
                total_amount += amount
                
                # You may need to handle date separately if it's not included in the OCR text
                # For now, I'll leave it as None
                date = None
                
                # Create a dictionary for the item
                item_data = {
                    "name": name,
                    "quantity": quantity,
                    "date": date,
                    "amount": amount
                }
                
                extracted_items.append(item_data)
            
            # You can now do whatever you want with the extracted items and total amount
            # For demonstration, I'm just returning the extracted items and total amount as a response
            response_data = {
                "items": extracted_items,
                "total_amount": total_amount
            }
            return Response(response_data, status=200)


















# class FileUploadAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request, *args, **kwargs):
#         # Get the uploaded file
#         # import pdb; pdb.set_trace()
#         file_obj = request.FILES.get('image')
        
#         # Save the uploaded file
#         file_path = default_storage.save(file_obj.name, ContentFile(file_obj.read()))
        
#         # Perform OCR on the uploaded image
#         image = Image.open(default_storage.path(file_path))
#         extracted_text = pytesseract.image_to_string(image)
        
#         # print(extracted_text)
#         item_details = re.findall(r'([A-Z\s]+)\s+(\d+)\s+(\d+\.\d{2})', extracted_text)
        
#         # Initialize a list to store extracted items
#         extracted_items = []
        
#         total_amount = 0.0

#         # Extracted data for each item
#         for item in item_details:
#             name = item[0].strip()
#             quantity = int(item[1])
#             amount = float(item[2])
            

#             total_amount += amount
#             # You may need to handle date separately if it's not included in the OCR text
#             # For now, I'll leave it as None
#             date = None
            
#             # Create a dictionary for the item
#             item_data = {
#                 "name": name,
#                 "quantity": quantity,
#                 "date": date,
#                 "amount": amount
#             }
            
#             extracted_items.append(item_data)
        
#         # You can now do whatever you want with the extracted items, such as saving them to the database
#         # For demonstration, I'm just returning the extracted items as a response
#         return Response(extracted_items, status=200)