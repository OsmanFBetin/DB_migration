from fastapi import FastAPI, HTTPException, UploadFile, File
from db.database import get_database, get_engine
from db.models import HistoricalData, Base
import csv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List, Optional

app = FastAPI()

# Database Initialization
database = get_database()
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)
metadata = MetaData()

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

    data = await file.read()
    data = data.decode("utf-8")

    # Parse and insert data into the database
    async with database.transaction():
        conn = engine
        csv_reader = csv.DictReader(data.splitlines())
        query = insert(HistoricalData)
        values = [row for row in csv_reader]
        conn.execute(query, values)

    return JSONResponse(content={"message": "CSV data uploaded successfully"})

@app.post("/insert-batch-data/")
async def insert_batch_data(request: Request, data: List[dict]):
    async with database.transaction():
        conn = engine
        query = insert(HistoricalData)
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

    return JSONResponse(content={"data": [dict(row) for row in rows]})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
