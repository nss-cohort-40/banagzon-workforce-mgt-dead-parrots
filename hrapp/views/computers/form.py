import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.last_name,
            e.first_name,
            ec.id empcomp_id,
            ec.computer_id,
            ec.employee_id
        from hrapp_employee e
        left join hrapp_employeecomputer ec on ec.employee_id = e.id;
        """)

        return db_cursor.fetchall()  

@login_required
def computer_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'computers/form.html'
        context = {
          'all_employees': employees,
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            insert into hrapp_computer
            (
              make, purchase_date
            )
            values (?, ?)
            """,
            (form_data['make'], form_data['purchase_date']))
            
            computer_id = db_cursor.lastrowid
            
            if form_data['employee'] != "NULL":

                db_cursor.execute("""
                insert into hrapp_employeecomputer
                (
                  computer_id, employee_id
                )
                values (?, ?)
                """,
                (computer_id, form_data['employee']))
            
        return redirect(reverse('hrapp:computer_list'))
