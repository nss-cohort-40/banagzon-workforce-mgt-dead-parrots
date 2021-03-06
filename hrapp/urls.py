from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('computers/', computer_list, name='computer_list'),
    path('computers/form', computer_form, name='computer_form'),
    path('computers/<int:computer_id>/', computer_details, name='computer'),
    path('employees/', employee_list, name='employee_list'),
    path('employee/form', employee_form, name='employee_form'),
    path('training_programs/', training_program_list, name='training_programs'),
    path('training_program/form', training_program_form, name='training_program_form'),
    path('training_programs/<int:training_program_id>/', training_program_details, name='training_program_details'),
    path('employees/<int:employee_id>/', employee_details, name='employee'),
    path('training_programs/<int:training_program_id>/form/', training_program_edit_form, name='training_program_edit_form'),
    path('training_programs/<int:training_program_id>/', training_program_details, name='training_program'),
    path('training_programs/<int:training_program_id>/<int:employee_id>/', employee_training_program_details, name='employee_training_program'),
    path('emp_training_programs/<int:employee_id>/form', employee_program_form, name='emp_program_form'),
    path('departments/', department_list, name='department_list'),
    path('departments/form', department_form, name='department_form'),
    path('departments/<int:department_id>', department_details, name='department'),
    path('employees/<int:employee_id>/form/', employee_edit_form, name='employee_edit_form'),
]
