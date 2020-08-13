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
                e.id employee_id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id
            from hrapp_employee e
            WHERE e.id = ?
            """, (employee_id,))

            row = db_cursor.fetchall()
            print('thee dataset', row) 
            employee = Employee()
            employee.id = row[0]['employee_id']
            employee.first_name = row[0]['first_name']
            employee.last_name = row[0]['last_name']
            employee.start_date = row[0]['start_date']
            employee.is_supervisor = row[0]['is_supervisor']
            employee.department_id = row[0]['department_id']

            return employee
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
          e.id,
          e.first_name employee_first,
          e.last_name employee_last,
          ec.id as connection_id
        from hrapp_computer c
        join hrapp_employeecomputer ec on c.id = ec.computer_id
        join hrapp_employee e on e.id = ec.employee_id
        """)

        return db_cursor.fetchall()

@login_required
def employee_form(request):
  if request.method == 'GET':
    departments = get_departments()
    template = 'employees/form.html'
    context = {
        'all_departments': departments
    }

    return render(request, template, context)

@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = get_employees(employee_id)
        departments = get_departments()
        computers = get_computers()
        template = 'employees/form.html'
        context = {
            'employee': employee,
            'computers': computers,
            'all_departments': departments,
        }

        return render(request, template, context)