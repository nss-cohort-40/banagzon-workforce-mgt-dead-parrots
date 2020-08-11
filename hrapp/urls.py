from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', home, name='employee_list'),
    path('departments/', department_list, name='department_list'),
    path('computers/', home, name='computer_list'),
    path('training_programs', home, name='training_programs')
]
