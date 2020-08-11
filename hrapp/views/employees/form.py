import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from ..connection import Connection

def get_employees():
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
            select
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor
            from hrapp_employee e
            """)

            return db_cursor.fetchall()

@login_required
def employee_form(request):
  if request.method == 'GET':
    employees = get_employees()
    template = 'employees/form.html'
    context = {
        'all_employees': employees
    }

    return render(request, template, context)