import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from hrapp.models import Department
from hrapp.models import Computer
from hrapp.models import Training_program
from ..connection import Connection


def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)
    employee = Employee()
    employee.id = _row['employee_id']
    employee.first_name = _row['first_name']
    employee.last_name = _row['last_name']
    employee.start_date = _row['start_date']
    employee.is_supervisor = _row['is_supervisor']
    employee.department_id = _row['department_id']

    department = Department()
    department.dept_name = _row['dept_name']
    department.id = _row['department_id']

    computer = Computer()
    computer.make = _row['computer_make']
    computer.id = _row['computer_id']
    employee.computer = computer

    employee.training_programs = []

    training_program = Training_program()
    training_program.name = _row['training_program_name']
    training_program.id = _row['training_program_id']
    
    return (employee, training_program,)


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select
                e.id employee_id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id,
                d.dept_name,
                c.id as computer_id,
                tp.id as training_program_id,
                c.make as computer_make,
                tp.name as training_program_name,
                ec.id as employeecomputer_id,
                tp.start_date as training_program_start,
                tp.end_date as training_program_end,
                etp.id as employeetrainingprogram_id,
                d.id as department_id
            from hrapp_employee e
            LEFT JOIN hrapp_department d ON
            e.department_id = d.id
            LEFT JOIN hrapp_employeecomputer ec ON
            e.id = ec.employee_id 
            LEFT JOIN hrapp_employee_training_program etp ON
            e.id = etp.employee_id
            LEFT JOIN hrapp_computer c ON
            c.id = ec.computer_id
            LEFT JOIN hrapp_training_program tp ON
            tp.id = etp.training_program_id
            WHERE e.id = ?; 
            """, (employee_id,))

    all_employees = db_cursor.fetchall()
    employee_groups = {}
    for (employee, training_program) in all_employees:
        if employee.id not in employee_groups:
            employee_groups[employee.id] = employee
            if training_program not in employee_groups[employee.id].training_programs:
                employee_groups[employee.id].training_programs.append(training_program)
        else:
            if training_program not in employee_groups[employee.id].training_programs:
                employee_groups[employee.id].training_programs.append(training_program)
    return employee_groups[employee_id]


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
        employee = get_employee(employee_id)
        template = 'employees/detail.html'
    
        context = {
            'employee': employee
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

    if (
        "actual_method" in form_data
        and form_data["actual_method"] == "DELETE"
    ):
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            DELETE FROM hrapp_employee
            WHERE id = ?
            """, (employee_id,))

        return redirect(reverse('hrapp:employee_list'))

