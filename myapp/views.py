from django.http import HttpResponse
from .models import project, task
from django.shortcuts import render, redirect, get_object_or_404
from .forms import create_new_task, CreateNewProject
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


def index(request):
    login_form = LoginForm(request, data=request.POST if request.POST.get('form_type') == 'login' else None)
    register_form = RegisterForm(request.POST if request.POST.get('form_type') == 'register' else None)

    if request.method == 'POST':
        if request.POST.get('form_type') == 'login' and login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('projects')
        elif request.POST.get('form_type') == 'register' and register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('projects')

    return render(request, 'index.html', {
        'login_form': login_form,
        'register_form': register_form
    })

@login_required
def about(request):
    title = 'Bienvenido a mi pagina!!'
    username = 'DrkDev'
    return render(request, 'about.html', {
        'username': username,
        'title': title
    })

@login_required
def projects(request):
    user_projects = project.objects.filter(user=request.user)
    return render(request, 'projects/projects.html', {
        'projects': user_projects
    })

@login_required
def create(request):

    if request.method == "POST":
        resource = request.POST.get("resource") 

        if resource == "project":
            project_form = CreateNewProject(request.POST)
            task_form = create_new_task() 

            if project_form.is_valid():
                project_form.save(user=request.user)
                return redirect("projects")

        elif resource == "task":
            task_form = create_new_task(request.POST)
            project_form = CreateNewProject()  
            if task_form.is_valid():
                task = task_form.save()
                return redirect("project_detail", id=task.project.id)

    else:  
        project_form = CreateNewProject()
        task_form = create_new_task()

    return render(
        request,
        "projects/create.html",  
        {
            "project_form": project_form,
            "task_form": task_form,
        },
    )

@login_required
def project_detail(request, id):
    peoject_id = get_object_or_404(project, id=id)
    tasks = task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project_name' : peoject_id,
        'tasks' : tasks,
    })    

@login_required
def done_task(request, pk):
    task_pk = get_object_or_404(task, pk=pk)
    task_pk.done = not task_pk.done
    task_pk.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_task(request, pk):
    task_pk = get_object_or_404(task, pk=pk)
    task_pk.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_project(request, pk):
    project_pk = get_object_or_404(project, pk=pk)
    project_pk.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}!")
            return redirect('about')  
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Cuenta creada exitosamente. ¡Bienvenido {user.username}!")
            return redirect('login')
        else:
            # Mensaje general
            messages.error(request, "Por favor corrige los errores en el formulario.")

            # Mostrar errores específicos por campo
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        label = form.fields[field].label or field.capitalize()
                        messages.error(request, f"{label}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente")
    return redirect('login')
