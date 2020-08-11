import sqlite3
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from hrapp.models import Training_program
from ..connection import Connection

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

        template = 'training_programs/detail.html'
        context = {
          'training_program': training_program
        }

        return render(request, template, context)