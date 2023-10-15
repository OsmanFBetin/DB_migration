from fastapi import FastAPI, HTTPException, UploadFile, File
from db.database import get_database, get_engine
from db.models import Base, DepartmentData, JobData, HiredEmployeeData, EmployeeStats
import csv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, text
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List, Optional

from utils.columns_names import get_columns, get_table_class
import datetime

app = FastAPI()

# Database Initialization
database = get_database()
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    query = text("""
        SELECT department
                , job
                , max(case when quarter = 'Q1' then total_employees else 0 end) as Q1
                , max(case when quarter = 'Q2' then total_employees else 0 end) as Q2
                , max(case when quarter = 'Q3' then total_employees else 0 end) as Q3
                , max(case when quarter = 'Q4' then total_employees else 0 end) as Q4
        FROM  
        (SELECT d.department as department
                , j.job as job
                , case 
                        when 0 + strftime('%m', e.datetime) between 1 and 3 then 'Q1'
                        when 0 + strftime('%m', e.datetime) between 4 and 6 then 'Q2'
                        when 0 + strftime('%m', e.datetime) between 7 and 9 then 'Q3'
                        when 0 + strftime('%m', e.datetime) between 10 and 12 then 'Q4'
                 end as quarter
                , count(e.id) as total_employees
        FROM hired_employees as e
        LEFT JOIN jobs as j
        ON j.id = e.job_id
        LEFT JOIN departments as d
        ON d.id = e.department_id
        WHERE strftime('%Y', e.datetime) = '2021'
        GROUP BY department
                , job
                , quarter) tbl
        GROUP BY tbl.department
                 , tbl.job
        """
    )
    with engine.connect() as conn:
        results = conn.execute(query)

        # employee_stats = []
        # for row in results:
        #     department, job, q1, q2, q3, q4 = row
        #     employee_stats.append(
        #     EmployeeStats(
        #             department=department,
        #             job=job,
        #             Q1=q1,
        #             Q2=q2,
        #             Q3=q3,
        #             Q4=q4
        #     ))
        # print(employee_stats)
        return JSONResponse(content={"data": [dict(row) for row in results]})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
