import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from hrapp.models import Training_program
from .form import training_program_form
from ..connection import Connection
import datetime

def training_program_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            current_date = datetime.date.today()
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
            WHERE tp.start_date >= ?
            """, (current_date,))

            all_training_programs = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                training_program = Training_program()
                training_program.id = row['id']
                training_program.name = row['name']
                training_program.description = row['description']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.max_attendees = row['max_attendees']

                all_training_programs.append(training_program)

            all_training_programs.sort(key=lambda program: program.start_date)

        template = 'training_programs/list.html'
        context = {
          'all_training_programs': all_training_programs
        }
        
        return render(request, template, context)
        
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
            INSERT INTO hrapp_training_program
            (
              name, description, start_date, end_date, max_attendees
            )
            VALUES (?, ?, ?, ?, ?)
            """, (form_data['name'], form_data['description'], form_data['start_date'], form_data['end_date'], form_data['max_attendees']))

        return redirect(reverse('hrapp:training_programs_list'))
