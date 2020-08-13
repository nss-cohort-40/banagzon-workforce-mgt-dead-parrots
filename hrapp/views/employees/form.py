import sqlite3
from django.shortcuts import render
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
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id,
            from hrapp_employee e
            WHERE e.id = ?
            """, (employee_id,))

            return db_cursor.fetchall()

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

def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
         select
          c.id,
          c.make,
          c.purchase_date,
          c.decommission_date,
        from hrapp_computer c
        """)

        return db_cursor.fetchall()

@login_required
def employee_form(request):
  if request.method == 'GET':
    deparments = get_departments()
    template = 'employees/form.html'
    context = {
        'all_departments': deparments
    }

    return render(request, template, context)

@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = get_employees(employee_id)
        department = get_departments()
        computer = get_computers()

        template = 'employees/form.html'
        context = {
            'employee': employee,
            'department': department,
            'computer': computer,
            'all_employees': employee
        }

        return render(request, template, context)