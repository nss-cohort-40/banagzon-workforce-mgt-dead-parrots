import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Employee
from ..connection import Connection
from ..departments import create_department


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_department
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.dept_name,
            d.budget,
            e.first_name,
            e.last_name,
            e.is_supervisor,
            e.start_date
        from hrapp_department d
        join hrapp_employee e on d.id = e.department_id
        """)

        department_groups = {}
        all_departments = db_cursor.fetchall()

        for (department, employee) in all_departments:
            if department.id not in department_groups:
                department_groups[department.id] = department
                department_groups[department.id].employees.append(employee)
            else:
                department_groups[department.id].employees.append(employee)

        return department_groups[department_id]
        

@login_required
def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)

        template = 'departments/detail.html'
        context = {
            'department': department
        }

        return render(request, template, context)
