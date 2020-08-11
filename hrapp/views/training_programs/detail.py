import sqlite3
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from hrapp.models import Training_program
from hrapp.models import Employee
from ..connection import Connection

def get_employees_attending(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          etp.id,
          etp.employee_id,
          etp.training_program_id,
          u.first_name,
          u.last_name,
          tp.id as program_id,
          tp.name
        FROM hrapp_employee_training_program etp
        JOIN auth_user u on etp.employee_id = u.id
        JOIN hrapp_training_program tp on program_id = ?;
        """, (training_program_id))

        employees_attending = []
        dataset = db_cursor.fetchall()

        for row in dataset:
          employee = Employee()
          employee.first_name = row['first_name']
          employee.last_name = row['last_name']

          employees_attending.append(employee)
        
        return employees_attending

def get_training_program(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
          etp.id,
          etp.employee_id,
          etp.training_program_id,
          u.first_name,
          u.last_name,
          tp.id as program_id
        FROM hrapp_employee_training_program etp
        JOIN auth_user u on etp.employee_id = u.id
        JOIN hrapp_training_program tp on program_id = ?;
        """, (training_program_id))

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
        training_program.employees = get_employees_attending(training_program_id)

        template = 'training_programs/detail.html'
        context = {
          'training_program': training_program
        }

        return render(request, template, context)