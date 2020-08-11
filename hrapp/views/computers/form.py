import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection

def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
          c.id,
          c.make,
          c.purchase_date,
          c.decommission_date
        from hrapp_computer c
        """)

        return db_cursor.fetchall()

@login_required
def computer_form(request):
    if request.method == 'GET':
        computers = get_computers()
        template = 'computers/form.html'
        context = {
          'all_computers': computers
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
            
        return redirect(reverse('hrapp:computer_list'))
