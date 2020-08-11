import sqlite3
from django.shortcuts import render
from ..connection import Connection

def training_program_form(request):
    if request.method == 'GET':
        template = 'training_programs/form.html'
        return render(request, template)