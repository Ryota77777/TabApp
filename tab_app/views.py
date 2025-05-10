from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Tabel, Employee
from .forms import TabelForm, EmployeeForm
from django.db.models import Sum
from django.http import HttpResponse
from django.db.models import Count
import openpyxl
from .forms import EmployeeProfileForm




def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')  # Для аутентифицированных пользователей
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте данные.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  
            if user:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Ошибка валидации формы.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

# 1. Список всех табелей
@login_required
def tabel_list(request):
    tabels = Tabel.objects.all()
    return render(request, 'tabel_list.html', {'tabels': tabels})

# 2. Создание нового табеля
@login_required
def tabel_create(request):
    if request.method == 'POST':
        form = TabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabel_list')
    else:
        form = TabelForm()
    return render(request, 'tabel_create.html', {'form': form})

# 3. Список всех сотрудников
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# 4. Страница отчетов

@login_required
def report(request):
    total_hours = Tabel.objects.aggregate(total_hours=Sum('hours'))['total_hours'] or 0

    # Группировка по сотрудникам: сколько часов и смен
    employee_stats = (
        Employee.objects.annotate(
            total_hours=Sum('tabel__hours'),
            shift_count=Count('tabel')
        ).order_by('-total_hours')
    )

    return render(request, 'report.html', {
        'total_hours': total_hours,
        'employee_stats': employee_stats,
    })

# 5. Настройки пользователя
@login_required
def settings(request):
    try:
        # Попытка получить сотрудника по текущему пользователю
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # Если сотрудник не найден, создаем нового
        employee = Employee.objects.create(user=request.user, first_name=request.user.first_name, last_name=request.user.last_name, position="New Employee", date_joined=request.user.date_joined)
    
    if request.method == 'POST':
        # Если это POST-запрос, обрабатываем форму
        form = EmployeeProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Перенаправляем после успешного сохранения
    else:
        # Если это GET-запрос, показываем форму с текущими данными
        form = EmployeeProfileForm(instance=employee)

    return render(request, 'settings.html', {'form': form})

login_required
def profile_view(request):
    employee = Employee.objects.get(user=request.user)
    return render(request, 'profile.html', {'employee': employee})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_edit.html', {'form': form, 'employee': employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})

def export_attendance(request):
    # Создаём Excel-файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Табели"

    # Заголовки
    ws.append(['Сотрудник', 'Дата', 'Время прихода', 'Время ухода', 'Отработанные часы', 'Примечание'])

    # Данные из БД
    for record in Tabel.objects.select_related('employee').all():
        ws.append([
            f"{record.employee.first_name} {record.employee.last_name}",
            record.date.strftime("%d.%m.%Y"),
            record.time_in.strftime("%H:%M") if record.time_in else '',
            record.time_out.strftime("%H:%M") if record.time_out else '',
            record.hours if record.hours else '',
            record.note if record.note else ''
        ])

    # Подготовка ответа
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
    wb.save(response)
    return response
