import sqlite3
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from hrapp.models import Training_program
from hrapp.models import Employee
from ..connection import Connection
from ...helpers import date_bool


def get_employees_attending(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          e.id,
          e.first_name,
          e.last_name,
          tp.name
        FROM hrapp_employee_training_program etp
        LEFT JOIN hrapp_employee e on e.id = etp.employee_id
        LEFT JOIN hrapp_training_program tp on tp.id = etp.training_program_id
        WHERE tp.id = ?
        """, (training_program_id,))
        
        return db_cursor.fetchall()


def get_training_program(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          tp.id,
          tp.name,
          tp.description,
          tp.start_date,
          tp.end_date,
          tp.max_attendees
        FROM hrapp_training_program tp
        WHERE tp.id = ?
        """, (training_program_id,))

        return db_cursor.fetchone()


def training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        program_employees = get_employees_attending(training_program_id)
        program_hasnt_started = date_bool(training_program['start_date'])
        template = 'training_programs/detail.html'
        context = {
          'training_program': training_program,
          'program_employees': program_employees,
          'program_hasnt_started': program_hasnt_started
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST
        
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_training_program
                SET name = ?,
                    description = ?,
                    start_date = ?,
                    end_date = ?,
                    max_attendees = ?
                WHERE id = ?
                """,
                (
                    form_data['name'], form_data['description'],
                    form_data['start_date'], form_data['end_date'],
                    form_data["max_attendees"], training_program_id,
                ))

            return redirect(reverse('hrapp:training_programs'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE-PROGRAM"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_training_program
                WHERE id = ?
                """, (training_program_id,))

            return redirect(reverse('hrapp:training_programs'))


def employee_training_program_details(request, training_program_id, employee_id):
    form_data = request.POST
    if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE-EMPLOYEE"
        ):

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_employee_training_program
                WHERE training_program_id = ?
                AND employee_id = ?
                """, (training_program_id, employee_id,))

            training_program = get_training_program(training_program_id)
            program_employees = get_employees_attending(training_program_id)
            program_hasnt_started = date_bool(training_program['start_date'])
            template = 'training_programs/detail.html'
            context = {
            'training_program': training_program,
            'program_employees': program_employees,
            'program_hasnt_started': program_hasnt_started
            }

            return render(request, template, context)