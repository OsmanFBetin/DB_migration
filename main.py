from fastapi import FastAPI, HTTPException, UploadFile, File
from db.database import get_database, get_engine
from db.models import Base, DepartmentData, JobData, HiredEmployeeData
import csv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, text
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List, Optional

from utils.columns_names import get_columns, get_table_class
from utils.querys import get_query_1, get_query_2
import datetime

app = FastAPI()

# Database Initialization
database = get_database()
engine = get_engine()

# Create the tables
Base.metadata.create_all(bind=engine)
metadata = MetaData()
metadata.bind = engine

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.get("/")
async def read_main():
    return {"msg": "Welcome to the API Migration"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    filename = file.filename.split(".")[0]

    column_names = get_columns(filename)
    # Get the table class
    table_class = get_table_class(filename)

    data = await file.read()
    data = data.decode("utf-8")

    csv_lines = data.splitlines()
    csv_reader = csv.DictReader(csv_lines)

    # Parse and insert data into the database
    async with database.transaction():
        conn = engine
        csv_reader = csv.DictReader(data.splitlines(), fieldnames=column_names)
        query = insert(table_class)

        if filename == "hired_employees":
            values = []
            for row in csv_reader:
                try:
                    new_datetime = datetime.datetime.fromisoformat(row['datetime'])
                    new_datetime = new_datetime.replace(tzinfo=None)
                except:
                    new_datetime = datetime.datetime(1900, 1, 1, 1, 1, 1)

                parameters_udp = {'id': row['id'], 'name': row['name'],
                            'datetime' : new_datetime, 'department_id': row['department_id']
                            , 'job_id' : row['job_id']}

                values.append(parameters_udp)
        else:
            values = [row for row in csv_reader]

        conn.execute(query, values)

    return JSONResponse(content={"message": "CSV data uploaded successfully"})

@app.post("/insert-batch-data/")
async def insert_batch_data(request: Request, filename: str, data: List[dict]):
    async with database.transaction():
        conn = engine
        table_class = get_table_class(filename)
        query = insert(table_class)

        if filename == "hired_employees":
            values = []
            for row in data:
                try:
                    new_datetime = datetime.datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S")
                except:
                    raise ValueError(f"Error: Only datetime value")

                parameters_udp = {'id': row['id'], 'name': row['name'],
                            'datetime' : new_datetime, 'department_id': row['department_id']
                            , 'job_id' : row['job_id']}

                values.append(parameters_udp)
            conn.execute(query, values)
        
        else:
            conn.execute(query, data)

    return JSONResponse(content={"message": "Batch data inserted successfully"})


@app.get("/query-table/{table_name}")
async def query_table_by_name(table_name: str, limit: Optional[int] = None):
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)

    if not table.exists():
        raise HTTPException(status_code=400, detail=f"Table '{table_name}' does not exist.")

    query = select([table])
    if limit:
        query = query.limit(limit)
    
    conn = engine
    result = conn.execute(query)
    rows = result.fetchall()

    if table_name == "hired_employees":
        values = []
        for row in rows:
            try:
                print("row: ", row[2])
                new_datetime = str(row[2])
            except:
                raise ValueError(f"Error: Only datetime value")

            parameters_udp = {'id': row[0], 'name': row[1],
                        'datetime' : new_datetime, 'department_id': row[3]
                        , 'job_id' : row[4]}

            values.append(parameters_udp)
        return JSONResponse(content={"data": values})
    else:
        return JSONResponse(content={"data": [dict(row) for row in rows]})


@app.get("/employee_stats")
async def get_employees_hired_by_job():
    query_1 = get_query_1()
    query = text(query_1)
    with engine.connect() as conn:
        results = conn.execute(query)

        return JSONResponse(content={"data": [dict(row) for row in results]})
    

@app.get("/department_stats")
async def department_stats():
    query_2 = get_query_2()
    query = text(query_2)
    with engine.connect() as conn:
        results = conn.execute(query)

        return JSONResponse(content={"data": [dict(row) for row in results]})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
