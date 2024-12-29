from django.shortcuts import render,HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q 

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request, 'all_emp.html',context)

def add_emp(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept, role_id=role, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee Added Successfully')
    elif request.method=='GET':
        return render(request,"add_emp.html")
    else:
        return HttpResponse("An Exception Occured! Employee has not been added")

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employeed removes succesfully")
        except:
            return HttpResponse("Plzz enter a valid employee id")

    emps = Employee.objects.all()
    context={
        'emps':emps
    }
    return render(request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method == "POST":
        name = request.POST.get('name')  # Use get() to avoid KeyError
        dept = request.POST.get('dept')
        role = request.POST.get('role')
        
        emps = Employee.objects.all()  # Start with all employees

        # Applying the name filter condition with OR for first_name and last_name
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        # Apply department filter if specified
        if dept:
            emps = emps.filter(dept__name=dept)

        # Apply role filter if specified
        if role:
            emps = emps.filter(role__name=role)

        # Prepare the context and render the filtered list of employees
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')

    else:
        return HttpResponse('Invalid')