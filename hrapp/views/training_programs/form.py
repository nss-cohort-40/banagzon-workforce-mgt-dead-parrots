import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Training_program
from hrapp.models import Employee
from ..employees.details import get_employee
from .detail import get_training_program
from ..connection import Connection
from ...helpers import date_bool
import datetime

@login_required
def training_program_form(request):
    
    if request.method == 'GET':
        template = 'training_programs/form.html'
        return render(request, template)

@login_required
def training_program_edit_form(request, training_program_id):

    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        program_hasnt_started = date_bool(training_program['start_date'])
        if program_hasnt_started:
            template = 'training_programs/form.html'
            context = {
                'training_program': training_program,
                'program_hasnt_started': program_hasnt_started
            }
            return render(request, template, context)

        return redirect(reverse('hrapp:training_programs'))

def employee_program_form(request, employee_id):
        if request.method == 'GET':
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = create_training_programs
                current_date = datetime.date.today()
                db_cursor = conn.cursor()

                db_cursor.execute("""
                SELECT
                    tp.id,
                    tp.name,
                    tp.max_attendees,
                    etp.employee_id
                FROM hrapp_training_program tp
                LEFT JOIN hrapp_employee_training_program etp on tp.id = etp.training_program_id
                WHERE start_date >= ?
                """, (current_date,))

                dataset = db_cursor.fetchall()
                capable_of_enrolling = sort_assigned_programs(employee_id, dataset)
                
                template = 'training_programs/emp_program_form.html'
                context = {
                    'training_programs': capable_of_enrolling,
                    'employee_id': employee_id
                }

                return render(request, template, context)

        elif request.method == 'POST':
            form_data = request.POST
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO hrapp_employee_training_program
                (
                    employee_id, training_program_id
                )
                VALUES (?, ?)
                """,
                (employee_id, form_data['training_program']))

            employee = get_employee(employee_id)
            template = 'employees/detail.html'
        
            context = {
                'employee': employee
            }

            return render(request, template, context)

def create_training_programs(cursor, row):
    _row = sqlite3.Row(cursor, row)

    training_program = Training_program()
    training_program.id = _row["id"]
    training_program.name = _row["name"]
    training_program.max_attendees = _row["max_attendees"]

    employee = Employee()
    employee.id = _row['employee_id']

    return (training_program, employee,)

def sort_assigned_programs(employee_id, dataset):
    all_programs = {}
    currently_enrolled = []
    capable_of_enrolling = []

    for (training_program, employee) in dataset:
        if training_program.name not in all_programs:
            all_programs[training_program.name] = list()
        if employee.id == employee_id:
            currently_enrolled.append(training_program.name)
        else:
            all_programs[training_program.name].append(training_program)

    for key, value in all_programs.items():
        if key not in currently_enrolled and len(value) < value[0].max_attendees:
            capable_of_enrolling.append({'name': key, 'id': value[0].id})

    return capable_of_enrolling