import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from .detail import get_training_program
from ..connection import Connection
from ...helpers import date_bool

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