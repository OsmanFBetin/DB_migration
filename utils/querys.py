def get_query_1():
    query = """
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
        ORDER BY tbl.department
                , tbl.job
        """
    return query


def query_2():
    query = """
        SELECT final.id
            , final.department
            , final.num_employees_hired as hired
        FROM
        (SELECT tbl.*
            , avg(tbl.num_employees_hired) over() as avg_num_employees
        FROM
            (SELECT d.id
                , d.department
                , count(*) as num_employees_hired
            FROM hired_employees as e
            LEFT JOIN departments as d
            ON d.id = e.department_id
            WHERE strftime('%Y', e.datetime) = '2021'
            GROUP BY d.id
                , d.department
            ) tbl) final
        WHERE final.num_employees_hired > final.avg_num_employees
        ORDER BY final.num_employees_hired DESC
        """
    return query
