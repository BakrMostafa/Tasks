from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Project, Task, Note, KnowledgeBase, Message
from .forms import ProjectForm, TaskForm, NoteForm, KnowledgeBaseForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.http import JsonResponse

# Create your views here.

@login_required
def dashboard(request):
    context = {
        'recent_projects': Project.objects.filter(
            Q(owner=request.user) | Q(collaborators=request.user)
        ).distinct().order_by('-updated_at')[:5],
        
        'upcoming_tasks': Task.objects.filter(
            assigned_to=request.user,
            status__in=['TODO', 'IN_PROGRESS']
        ).order_by('due_date')[:5],
        
        'recent_notes': Note.objects.filter(
            owner=request.user
        ).order_by('-updated_at')[:5],
        
        'stats': {
            'total_projects': Project.objects.filter(
                Q(owner=request.user) | Q(collaborators=request.user)
            ).distinct().count(),
            'pending_tasks': Task.objects.filter(
                assigned_to=request.user,
                status__in=['TODO', 'IN_PROGRESS']
            ).count(),
            'completed_tasks': Task.objects.filter(
                assigned_to=request.user,
                status='COMPLETED'
            ).count(),
        }
    }
    return render(request, 'website/dashboard.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(collaborators=request.user)
    ).distinct().order_by('-updated_at')
    
    context = {
        'projects': projects,
        'active_projects_count': projects.filter(status='ACTIVE').count(),
        'on_hold_projects_count': projects.filter(status='ON_HOLD').count(),
        'completed_projects_count': projects.filter(status='COMPLETED').count(),
    }
    
    return render(request, 'website/projects.html', context)

@login_required
def task_list(request):
    tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(project__owner=request.user)
    ).order_by('-created_at')
    return render(request, 'website/tasks.html', {'tasks': tasks})

@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user).order_by('-updated_at')
    return render(request, 'website/notes.html', {'notes': notes})

@login_required
def knowledge_base(request):
    query = request.GET.get('q', '')
    articles = KnowledgeBase.objects.all()
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    articles = articles.order_by('-updated_at')
    return render(request, 'website/knowledge.html', {'articles': articles})

@login_required
def global_search(request):
    query = request.GET.get('q', '')
    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        knowledge_base = KnowledgeBase.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        projects = tasks = notes = knowledge_base = []

    context = {
        'query': query,
        'projects': projects,
        'tasks': tasks,
        'notes': notes,
        'knowledge_base': knowledge_base
    }
    return render(request, 'website/search_results.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Successfully logged in!'))
                return redirect('dashboard')
        else:
            messages.error(request, _('Invalid username or password.'))
    else:
        form = AuthenticationForm()
    
    return render(request, 'website/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, _('Successfully logged out!'))
        return redirect('login')
    return render(request, 'website/logout.html')

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            messages.success(request, _('Registration successful!'))
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'website/register.html', {'form': form})

def password_reset(request):
    return render(request, 'website/password_reset.html')

def index_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, _('Project created successfully!'))
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    
    return render(request, 'website/project_form.html', {'form': form, 'action': 'Create'})

@login_required
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if not (request.user == project.owner or request.user in project.collaborators.all()):
        raise PermissionDenied
    
    # Get all tasks for this project
    tasks = Task.objects.filter(project=project).order_by('-updated_at')
    
    # Get all files for this project
    files = project.files.all().order_by('-uploaded_at')
    
    # Get all notes for this project
    notes = project.project_notes.all().order_by('-updated_at')
    
    # Calculate task statistics
    tasks_in_progress = tasks.filter(status='IN_PROGRESS').exists()
    tasks_in_review = tasks.filter(status='REVIEW').exists()
    completion_percentage = project.completion_percentage()
    
    context = {
        'project': project,
        'tasks': tasks,
        'files': files,
        'notes': notes,
        'completion_percentage': completion_percentage,
        'tasks_in_progress': tasks_in_progress,
        'tasks_in_review': tasks_in_review,
        'tasks_count': {
            'total': tasks.count(),
            'open': tasks.filter(status__in=['TODO', 'IN_PROGRESS', 'REVIEW']).count(),
            'completed': tasks.filter(status='DONE').count(),
        },
        'files_count': files.count(),
        'notes_count': notes.count(),
        'collaborators_count': project.collaborators.count() + 1  # +1 for owner
    }
    
    return render(request, 'website/project_detail.html', context)

@login_required
def load_project_chat(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if not (request.user == project.owner or request.user in project.collaborators.all()):
        raise PermissionDenied
    
    messages = Message.objects.filter(project=project).order_by('created_at')
    
    messages_data = []
    for message in messages:
        message_data = {
            'content': message.content,
            'sender': message.sender.username,
            'created_at': message.created_at.strftime('%b %d, %Y %I:%M %p'),
            'is_own': message.sender == request.user
        }
        
        if message.attachment:
            message_data.update({
                'attachment_url': message.attachment.url,
                'attachment_type': message.attachment_type,
                'attachment_name': message.attachment_name or message.attachment.name
            })
        
        messages_data.append(message_data)
    
    return JsonResponse({'messages': messages_data})

@login_required
def project_update(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.user != project.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, _('Project updated successfully!'))
            return redirect('project_detail', slug=project.slug)
        else:
            messages.error(request, _('Please correct the errors below.'))
    
    # If it's a GET request or form is invalid, return to the project detail page
    return redirect('project_detail', slug=project.slug)

@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.user != project.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, _('Project deleted successfully!'))
        return redirect('projects')
    
    # If it's a GET request, return to the project detail page
    return redirect('project_detail', slug=project.slug)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # Check if user has permission to create task in this project
            project = form.cleaned_data['project']
            if not (request.user == project.owner or request.user in project.collaborators.all()):
                raise PermissionDenied
            task.save()
            messages.success(request, _('Task created successfully!'))
            return redirect('task_detail', pk=task.pk)
    else:
        initial_project = request.GET.get('project')
        form = TaskForm(initial={'project': initial_project} if initial_project else None)
    
    return render(request, 'website/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not (request.user == task.project.owner or request.user == task.assigned_to):
        raise PermissionDenied
    
    return render(request, 'website/task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not (request.user == task.project.owner or request.user == task.assigned_to):
        raise PermissionDenied
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task updated successfully!'))
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'website/task_form.html', {'form': form, 'action': 'Update'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.project.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        project_slug = task.project.slug
        task.delete()
        messages.success(request, _('Task deleted successfully!'))
        return redirect('project_detail', slug=project_slug)
    
    return render(request, 'website/task_confirm_delete.html', {'task': task})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            form.save_m2m()  # Save tags
            messages.success(request, _('Note created successfully!'))
            return redirect('note_detail', pk=note.pk)
    else:
        initial_project = request.GET.get('project')
        initial_task = request.GET.get('task')
        form = NoteForm(initial={
            'project': initial_project,
            'task': initial_task
        })
    
    return render(request, 'website/note_form.html', {'form': form, 'action': 'Create'})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user != note.owner:
        raise PermissionDenied
    return render(request, 'website/note_detail.html', {'note': note})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user != note.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, _('Note updated successfully!'))
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'website/note_form.html', {'form': form, 'action': 'Update'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user != note.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, _('Note deleted successfully!'))
        return redirect('notes')
    
    return render(request, 'website/note_confirm_delete.html', {'note': note})

@login_required
def knowledge_base_create(request):
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # Save tags
            messages.success(request, _('Article created successfully!'))
            return redirect('knowledge_base_detail', pk=article.pk)
    else:
        form = KnowledgeBaseForm()
    
    return render(request, 'website/knowledge_base_form.html', {'form': form, 'action': 'Create'})

@login_required
def knowledge_base_detail(request, pk):
    article = get_object_or_404(KnowledgeBase, pk=pk)
    return render(request, 'website/knowledge_base_detail.html', {'article': article})

@login_required
def knowledge_base_update(request, pk):
    article = get_object_or_404(KnowledgeBase, pk=pk)
    if request.user != article.author:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, _('Article updated successfully!'))
            return redirect('knowledge_base_detail', pk=article.pk)
    else:
        form = KnowledgeBaseForm(instance=article)
    
    return render(request, 'website/knowledge_base_form.html', {'form': form, 'action': 'Update'})

@login_required
def knowledge_base_delete(request, pk):
    article = get_object_or_404(KnowledgeBase, pk=pk)
    if request.user != article.author:
        raise PermissionDenied
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, _('Article deleted successfully!'))
        return redirect('knowledge')
    
    return render(request, 'website/knowledge_base_confirm_delete.html', {'article': article})

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile info
        profile.employee_id = request.POST.get('employee_id', '')
        profile.user_type = request.POST.get('user_type', 'JUNIOR')
        profile.job_title = request.POST.get('job_title', '')
        profile.github_username = request.POST.get('github_username', '')
        profile.mobile_phone = request.POST.get('mobile_phone', '')
        profile.primary_skills = request.POST.get('primary_skills', '')
        profile.bio = request.POST.get('bio', '')
        profile.department = request.POST.get('department', '')
        profile.github_profile = request.POST.get('github_profile', '')
        profile.linkedin_profile = request.POST.get('linkedin_profile', '')
        profile.timezone = request.POST.get('timezone', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, _('Profile updated successfully!'))
        return redirect('profile')

    # Calculate project statistics
    user_projects = Project.objects.filter(
        Q(owner=request.user) | Q(collaborators=request.user)
    ).distinct()
    
    project_stats = {
        'total': user_projects.count(),
        'active': user_projects.filter(tasks__status__in=['TODO', 'IN_PROGRESS']).distinct().count(),
        'completed': user_projects.exclude(tasks__status__in=['TODO', 'IN_PROGRESS']).distinct().count(),
    }

    # Calculate task statistics
    user_tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(project__owner=request.user)
    )
    
    completed_tasks = user_tasks.filter(status='DONE').count()
    total_tasks = user_tasks.count()
    on_time_tasks = user_tasks.filter(
        status='DONE',
        due_date__gte=models.F('updated_at')
    ).count()

    task_stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
        'on_time_rate': round((on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0, 1)
    }

    context = {
        'user': request.user,
        'profile': request.user.profile,
        'project_stats': project_stats,
        'task_stats': task_stats,
    }
    return render(request, 'website/profile.html', context)

@login_required
def project_github_connect(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.user != project.owner:
        raise PermissionDenied
    
    if request.method == 'POST':
        github_repo = request.POST.get('github_repo')
        github_token = request.POST.get('github_token')
        
        # Validate GitHub repo and token
        # Add GitHub API integration code here
        
        project.github_repo = github_repo
        project.github_access_token = github_token
        project.is_github_connected = True
        project.save()
        
        messages.success(request, _('GitHub repository connected successfully!'))
        return redirect('project_detail', slug=project.slug)
    
    return render(request, 'website/project_github_connect.html', {'project': project})

@login_required
def settings_view(request):
    context = {
        'github_connected': bool(request.user.profile.github_access_token),
        'notification_settings': {
            'email_notifications': request.user.profile.email_notifications,
            'desktop_notifications': request.user.profile.desktop_notifications,
            'mention_notifications': request.user.profile.mention_notifications,
        },
        'appearance_settings': {
            'theme': request.user.profile.theme,
            'sidebar_collapsed': request.user.profile.sidebar_collapsed,
            'code_theme': request.user.profile.code_theme,
        },
        'integration_tokens': {
            'github': bool(request.user.profile.github_access_token),
            'gitlab': bool(request.user.profile.gitlab_access_token),
            'jira': bool(request.user.profile.jira_access_token),
        }
    }
    return render(request, 'website/settings.html', context)

@login_required
def appearance_settings(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        sidebar_collapsed = request.POST.get('sidebar_collapsed') == 'on'
        code_theme = request.POST.get('code_theme')
        
        profile = request.user.profile
        profile.theme = theme
        profile.sidebar_collapsed = sidebar_collapsed
        profile.code_theme = code_theme
        profile.save()
        
        messages.success(request, _('Appearance settings updated successfully!'))
        return redirect('settings')
    
    return redirect('settings')

@login_required
def integration_settings(request):
    if request.method == 'POST':
        integration_type = request.POST.get('integration_type')
        access_token = request.POST.get('access_token')
        
        profile = request.user.profile
        if integration_type == 'github':
            profile.github_access_token = access_token
        elif integration_type == 'gitlab':
            profile.gitlab_access_token = access_token
        elif integration_type == 'jira':
            profile.jira_access_token = access_token
            
        profile.save()
        messages.success(request, _(f'{integration_type.title()} integration updated successfully!'))
        return redirect('settings')
    
    return redirect('settings')

@login_required
def notification_settings(request):
    if request.method == 'POST':
        email_notifications = request.POST.get('email_notifications') == 'on'
        desktop_notifications = request.POST.get('desktop_notifications') == 'on'
        mention_notifications = request.POST.get('mention_notifications') == 'on'
        
        profile = request.user.profile
        profile.email_notifications = email_notifications
        profile.desktop_notifications = desktop_notifications
        profile.mention_notifications = mention_notifications
        profile.save()
        
        messages.success(request, _('Notification settings updated successfully!'))
        return redirect('settings')
    
    return redirect('settings')

@login_required
def messages_view(request):
    # Get all conversations where user is either sender or recipient
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user),
        project__isnull=True  # Only direct messages
    ).values('sender', 'recipient').distinct()
    
    users_with_conversations = set()
    for conv in conversations:
        users_with_conversations.add(conv['sender'])
        users_with_conversations.add(conv['recipient'])
    users_with_conversations.discard(request.user.id)
    
    chat_users = User.objects.filter(id__in=users_with_conversations)
    
    context = {
        'chat_users': chat_users,
    }
    return render(request, 'website/messages.html', context)

@login_required
def chat_detail(request, user_id=None, project_slug=None):
    if user_id:
        other_user = get_object_or_404(User, id=user_id)
        messages = Message.objects.filter(
            (Q(sender=request.user, recipient=other_user) | 
             Q(sender=other_user, recipient=request.user)),
            project__isnull=True
        ).order_by('created_at')
        context = {
            'other_user': other_user,
            'messages': messages,
            'chat_type': 'direct'
        }
    else:
        project = get_object_or_404(Project, slug=project_slug)
        if not (request.user == project.owner or request.user in project.collaborators.all()):
            raise PermissionDenied
        messages = Message.objects.filter(project=project).order_by('created_at')
        context = {
            'project': project,
            'messages': messages,
            'chat_type': 'project'
        }
    
    return render(request, 'website/chat_detail.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        recipient_id = request.POST.get('recipient_id')
        project_slug = request.POST.get('project_slug')
        attachment = request.FILES.get('attachment')
        
        message_data = {
            'sender': request.user,
            'content': content
        }
        
        # Handle attachment if present
        if attachment:
            message_data['attachment'] = attachment
            message_data['attachment_name'] = attachment.name
            
            # Determine attachment type
            content_type = attachment.content_type
            if content_type.startswith('image/'):
                message_data['attachment_type'] = 'IMAGE'
            elif content_type.startswith('video/'):
                message_data['attachment_type'] = 'VIDEO'
            else:
                message_data['attachment_type'] = 'FILE'
        
        if project_slug:
            project = get_object_or_404(Project, slug=project_slug)
            if not (request.user == project.owner or request.user in project.collaborators.all()):
                raise PermissionDenied
            message_data['project'] = project
        else:
            recipient = get_object_or_404(User, id=recipient_id)
            message_data['recipient'] = recipient
        
        message = Message.objects.create(**message_data)
        
        response_data = {
            'status': 'success',
            'message': {
                'id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'created_at': message.created_at.strftime('%b %d, %Y %H:%M')
            }
        }
        
        if message.attachment:
            response_data['message'].update({
                'attachment_url': message.attachment.url,
                'attachment_type': message.attachment_type,
                'attachment_name': message.attachment_name
            })
        
        return JsonResponse(response_data)
    
    return JsonResponse({'status': 'error'}, status=400)
