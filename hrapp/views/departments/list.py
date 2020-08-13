import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from hrapp.models import Department
from hrapp.models import Employee
from ..connection import Connection

def create_department(cursor, row):
    _row = sqlite3.Row(cursor, row)

    department = Department()
    department.id = _row["id"]
    department.dept_name = _row["dept_name"]
    department.budget = _row["budget"]
    department.employees = []

    employee = Employee()
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.is_supervisor = _row["is_supervisor"]
    employee.start_date = _row["start_date"]

    return (department, employee,)
    
def department_list(request):
    if request.method == 'GET':
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
            left join hrapp_employee e on d.id = e.department_id;
            """)

            all_departments = db_cursor.fetchall()

            department_groups = {}

            for (department, employee) in all_departments:
                if department.id not in department_groups:
                    department_groups[department.id] = department
                    department_groups[department.id].employees.append(employee)
                else:
                    department_groups[department.id].employees.append(employee)

        template = 'departments/list.html'
        context = {
            'departments': department_groups.values(),
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_department
            (dept_name, budget)
            VALUES (?, ?)
            """,
            (form_data['dept_name'], form_data['budget']))

        return redirect(reverse('hrapp:department_list'))