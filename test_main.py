import io
import csv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome to the API Migration"}

def test_upload_csv():
    # Create a mock CSV file as a bytes object
    csv_data = "186,Developer AWS I\n187,Developer Azure I".encode("utf-8")

    csv_file = io.BytesIO(csv_data)

    # Send a POST request to the endpoint with the mock CSV file
    response = client.post("/upload-csv/", files={"file": ("jobs.csv", csv_file, "application/json")})

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json() == {"message": "CSV data uploaded successfully"}