import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from hrapp.models import Department
from ..connection import Connection


def get_employees(employee_id):
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                e.id employee_id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id
            from hrapp_employee e
            WHERE e.id = ?
            """, (employee_id,))

            return db_cursor.fetchone()

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.dept_name,
            d.budget
        from hrapp_department d
        """)

        return db_cursor.fetchall()

@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employees(employee_id)

        template = 'employees/detail.html'
        context = {
            'employee': employee
        }

        return render(request, template, context)