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
    path('employees/', home, name='employee_list'),
    path('departments/', home, name='department_list'),
    path('training_programs/', training_program_list, name='training_programs'),
    path('training_program/form', training_program_form, name='training_program_form'),
    path('training_programs/<int:training_program_id>/', training_program_details, name='training_program_details'),
]
