import csv
import os
import shutil
from typing import Dict
from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
from pdf_service import PdfService

app = FastAPI()

pdf_service = PdfService(key="TEST_KEY")

@app.get("/")
def read_root():
    """
    This function retrieves the data from a PDF file and compares it with the stored data.

    Parameters:
    None

    Returns:
    A JSONResponse object containing a summary of the comparison between the extracted data and the stored data.

    Raises:
    HTTPException with status code 400 if the file provided is invalid.

    Usage:
    The function is called when the root path ("/") is accessed. It retrieves the data from the "healthinc.pdf" file located in the "assets" directory.

    If the extracted data or the stored data is empty, an empty summary with a 200 status code is returned. Otherwise, the function compares the extracted data with the stored data and returns a JSONResponse object containing a summary of the comparison.
    """
    file_location = "assets/healthinc.pdf"

    try:
        extracted_data = pdf_service.extract(file_path=file_location)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cannot extract data. Invalid file provided.")
    
    stored_data = get_stored_data('HealthInc')
    
    # If either extracted_data or stored_data is empty, return an empty summary with a 200 status code
    if not extracted_data or not stored_data:
        return JSONResponse(content={"summary": {}}, status_code=200)
    
    summary = compare_data(extracted_data, stored_data)
    return JSONResponse(content={"summary": summary})

@app.post("/upload/")
async def upload_pdf(company_name: str = Form(...), file: UploadFile = File(...)):
    file_location = f"assets/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        extracted_data = pdf_service.extract(file_location)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cannot extract data. Invalid file provided.")
    finally:
        os.remove(file_location)  # Clean up the saved file
    
    stored_data = get_stored_data(company_name)
    if not stored_data:
        raise HTTPException(status_code=404, detail="Company data not found.")
    
    summary = compare_data(extracted_data, stored_data)
    return JSONResponse(content={"summary": summary})

# Cache dictionary: this mocks a possible cache implementation
cache = {}

def csv_to_dict(file_path):
    """
    This function reads a CSV file and converts it into a dictionary.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    dict: A dictionary where the keys are the 'Company Name' from the CSV file and the values are the corresponding rows.

    Raises:
    FileNotFoundError: If the CSV file is not found.

    Usage:
    The function is called with the path to the CSV file as an argument. It reads the file, converts it into a dictionary, and returns the dictionary.

    If the file path is already in the cache and the file has not been modified since caching, the function returns the cached dictionary.
    """
    # Check if the file path is in cache and the file has not been modified since caching
    if file_path in cache:
        file_stat = os.stat(file_path)
        if cache[file_path]['mtime'] == file_stat.st_mtime:
            return cache[file_path]['data']
    
    result = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                company_name = row.get('Company Name')
                for key in row:
                    if row[key].replace('.', '', 1).isdigit():
                        row[key] = float(row[key]) if '.' in row[key] else int(row[key])
                result[company_name] = row
        file_stat = os.stat(file_path)
        cache[file_path] = {
            'data': result,
            'mtime': file_stat.st_mtime
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    return result

def get_stored_data(company_name):
    """
    This function retrieves the data for a specific company from the 'database.csv' file.

    Parameters:
    company_name (str): The name of the company for which the data needs to be retrieved.

    Returns:
    dict: A dictionary containing the data for the specified company, or None if the company is not found.

    Raises:
    FileNotFoundError: If the 'database.csv' file is not found.
    Exception: If any other error occurs during the retrieval process.

    Usage:
    The function is called with the name of the company as an argument. It reads the 'database.csv' file, converts it into a dictionary, and returns the data for the specified company.

    If the 'database.csv' file is not found, a FileNotFoundError is raised. If any other error occurs during the retrieval process, an Exception is raised.
    """
    file_path = 'data/database.csv'
    try:
        data = csv_to_dict(file_path)
        return data.get(company_name)
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found")
    except Exception as e:
        raise e
    
def compare_data(extracted_data: Dict, stored_data: Dict) -> Dict:
    """
    This function compares the extracted data with the stored data and returns a summary of the comparison.

    Parameters:
    extracted_data (Dict): A dictionary containing the extracted data from the PDF file.
    stored_data (Dict): A dictionary containing the stored data for comparison.

    Returns:
    Dict: A dictionary containing the comparison summary for each key in both dictionaries. The summary includes the extracted value, the stored value, and a boolean indicating whether the values match.

    Usage:
    The function is called with the extracted data and the stored data as arguments. It compares the values for each key in both dictionaries and returns a dictionary containing the comparison summary.
    """
    summary = {}
    all_keys = set(extracted_data.keys()).union(set(stored_data.keys()))
    
    for key in all_keys:
        extracted_value = extracted_data.get(key, None)
        stored_value = stored_data.get(key, None)
        summary[key] = {
            "extracted": extracted_value,
            "stored": stored_value,
            "match": extracted_value == stored_value
        }
        
    return summary
