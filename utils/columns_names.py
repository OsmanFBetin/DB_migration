from db.models import Base, DepartmentData, JobData, HiredEmployeeData

def get_columns(key):
    columns = {
        "departments" : ["id", "department"]
        , "jobs" : ["id", "job"]
        , "hired_employees" : ["id", "name", "datetime", "department_id", "job_id"]
    }

    try:
        return columns[key]
    except KeyError:
        raise KeyError(f"Key {key} not found in the columns dictionary.")


def get_table_class(key):
    tables = {
        "departments" : DepartmentData
        , "jobs" : JobData
        , "hired_employees" : HiredEmployeeData
    }

    try:
        return tables[key]
    except KeyError:
        raise KeyError(f"Key {key} not found in the table dictionary.")
