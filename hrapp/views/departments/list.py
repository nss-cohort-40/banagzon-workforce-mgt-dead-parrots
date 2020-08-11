import sqlite3
from django.shortcuts import render
from hrapp.models import Department


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect("/Users/zanebliss/workspace/back-end/banagzon-workforce-mgt-dead-parrots/db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                d.id,
                d.dept_name,
                d.budget
            from hrapp_department d
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.dept_name = row['dept_name']
                department.budget = row['budget']

                all_departments.append(department)

    template = 'departments/list.html'
    context = {
        'departments': all_departments
    }

    return render(request, template, context)
