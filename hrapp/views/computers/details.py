import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from ..connection import Connection

def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
          c.id,
          c.make,
          c.purchase_date,
          c.decommission_date,
          e.id,
          e.first_name,
          e.last_name
        from hrapp_computer c
        join hrapp_employeecomputer ec on c.id = ec.computer_id
        join hrapp_employee e on e.id = ec.employee_id
        where c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()

@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)

        template = 'computers/detail.html'
        context = {
            'computer': computer
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == 'DELETE'
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                delete from hrapp_computer
                where id = ?
                """, (computer_id,))

            return redirect(reverse('hrapp:computer_list'))
