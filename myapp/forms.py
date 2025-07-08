from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import project, task


class create_new_task(forms.Form):
    title = forms.CharField(label="Titulo de la tarea", max_length=200, required=True,
                             widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label="Descripcion de la tarea",
                                  widget=forms.Textarea(attrs={'class': 'input'}))
    project = forms.ModelChoiceField(
        queryset=project.objects.all(),
        label="¿A qué proyecto pertenece?",
        widget=forms.Select(attrs={'class': 'input project-selector'})
    )

    def save(self):
        data = self.cleaned_data
        return task.objects.create(
            title=data['title'],
            description=data['description'],
            project=data['project']
        )


class CreateNewProject(forms.Form):
    name = forms.CharField(label="Titulo del proyecto", max_length=200, required=True,
                           widget=forms.TextInput(attrs={'class': 'input'}))

    def save(self, user): 
        from .models import project  
        return project.objects.create(
            name=self.cleaned_data['name'],
            user=user  
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "input"})
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input"})
    )


class RegisterForm(UserCreationForm):
    # Campos que has definido explícitamente
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-largo"})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={"class": "input-largo"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input-largo"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input-largo"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
