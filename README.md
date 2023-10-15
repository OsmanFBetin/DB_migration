## BD_Migration API Documentation

**Introduction:**

BD_Migration is a public API built with the FastAPI framework, which allows users to efficiently migrate historical data from CSV files to a new database. It provides several endpoints to facilitate data migration, batch transaction inserts, and data analysis.

### Getting Started

1. **Project Repository:**

   To use BD_Migration, start by downloading the full project from the GitHub repository:
   [BD_Migration Repository](https://github.com/OsmanFBetin/DB_migration)

2. **Install Dependencies:**

   Make sure to install all the necessary dependencies listed in the `requirements.txt` file.

3. **Start the Web Server:**

   BD_Migration is designed to work with Uvicorn as the web server. Start the web server to make the API accessible.

   ```bash
   uvicorn main:app --reload
   ```

4. **Access FastAPI Swagger:**

   Open a web browser and navigate to the local URL for FastAPI Swagger. This is where you can interact with the API endpoints and explore its functionality.

   ![swagger](https://github.com/OsmanFBetin/DB_migration/assets/137963525/0feae147-5080-418f-b1b6-b424ba5789dd)

### API Endpoints

BD_Migration provides the following endpoints to perform various operations:

#### 1. /upload-csv

- **Description:**
  This endpoint allows you to upload historical data from three different CSV files: `departments.csv`, `jobs.csv`, and `hired_employees.csv`. It performs a full load of this data into the database using the model defined in this application (`models.py`).

- **Usage:**
  Upload historical data from CSV files to the new database.

- **Endpoint URL:**
  `http://localhost:8000/upload-csv`

- **HTTP Method:**
  POST

![upload](https://github.com/OsmanFBetin/DB_migration/assets/137963525/bbeea2e4-2427-44e4-8a46-9e2b943cad10)

#### 2. /insert-batch-data

- **Description:**
  Use this endpoint to insert batch transactions, which allows you to insert multiple rows with a single request.

- **Usage:**
  Efficiently insert a batch of data (1 up to 1000 rows) with a single API request.

- **Endpoint URL:**
  `http://localhost:8000/insert-batch-data`

- **HTTP Method:**
  POST

![batch](https://github.com/OsmanFBetin/DB_migration/assets/137963525/21878217-9097-4081-91d4-95c4584953cd)

#### 3. /query-table/{table_name}

- **Description:**
  This endpoint is designed to quickly inspect the data loaded in a specific table. You can use it to view the contents of the specified table.

- **Usage:**
  Inspect the data in a particular table within the database.

- **Endpoint URL:**
  `http://localhost:8000/query-table/{table_name}`

- **HTTP Method:**
  GET

![query_table](https://github.com/OsmanFBetin/DB_migration/assets/137963525/ec5b01b1-406f-404a-9ef1-c78df4037cf2)

#### 4. /employee_stats

- **Description:**
  Use this endpoint to retrieve statistics about the number of employees hired for each job and department in the year 2021, divided by quarter. The results are ordered alphabetically by department and job.

- **Usage:**
  Obtain detailed employee statistics for 2021 by job and department.

- **Endpoint URL:**
  `http://localhost:8000/employee_stats`

- **HTTP Method:**
  GET

![employee_stats](https://github.com/OsmanFBetin/DB_migration/assets/137963525/8c0f91ff-5992-46c5-842e-0b492ca6950f)

#### 5. /departments_stats

- **Description:**
  This endpoint provides a list of department IDs, names, and the number of employees hired for each department that hired more employees than the mean of employees hired in 2021 across all departments. The results are ordered by the number of employees hired in descending order.

- **Usage:**
  Retrieve information about departments that hired more employees than the mean for 2021.

- **Endpoint URL:**
  `http://localhost:8000/departments_stats`

- **HTTP Method:**
  GET

![department_stats](https://github.com/OsmanFBetin/DB_migration/assets/137963525/c5eeae7f-527a-4760-8bd1-efc0b372b1db)
