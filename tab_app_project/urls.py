from django.contrib import admin
from django.urls import path, include
from tab_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tab_app.urls')),  
    path('', include('tab_app.urls')),  
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.user_login, name='login'),  # Страница входа
    path('register/', views.user_register, name='register'),  # Страница регистрации
    path('logout/', views.user_logout, name='logout'),  # Выход из системы
    path('tabel/', views.tabel_list, name='tabel_list'),
    path('tabel/create/', views.tabel_create, name='tabel_create'),
    path('employees/', views.employee_list, name='employee_list'),
    path('reports/', views.report, name='report'),
    path('profile/', views.profile_view, name='profile'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('export/', views.export_attendance, name='export_attendance'),
    path('settings/', views.settings, name='settings')
]

