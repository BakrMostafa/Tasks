from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects')
    github_repo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    github_branch = models.CharField(max_length=100, default='main', blank=True)
    github_organization = models.CharField(max_length=100, blank=True)
    github_project_name = models.CharField(max_length=100, blank=True)
    github_access_token = models.CharField(max_length=255, blank=True)
    is_github_connected = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('ACTIVE', 'Active'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVED', 'Archived')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(uuid.uuid4())[:8])
        super().save(*args, **kwargs)

    def completion_percentage(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='DONE').count()
        return round((completed_tasks / total_tasks) * 100)

    def days_remaining(self):
        if not self.tasks.exists():
            return 0
        latest_due_date = self.tasks.filter(due_date__isnull=False).order_by('-due_date').first()
        if not latest_due_date:
            return 0
        remaining = (latest_due_date.due_date.date() - timezone.now().date()).days
        return max(0, remaining)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent')
    ]
    
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('REVIEW', 'In Review'),
        ('DONE', 'Done')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    @property
    def duration_display(self):
        if not self.start_date:
            return "Not started"
        
        end_date = self.completion_date if self.completion_date else timezone.now()
        duration = end_date - self.start_date
        
        days = duration.days
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            
        return ", ".join(parts) if parts else "Less than a minute"

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='project_notes',
        null=True,
        blank=True
    )
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#000000")

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='project_files/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class KnowledgeBase(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('JUNIOR', 'Junior Developer'),
        ('MID', 'Mid-Level Developer'),
        ('SENIOR', 'Senior Developer'),
        ('LEAD', 'Team Lead'),
        ('MANAGER', 'Project Manager'),
        ('ARCHITECT', 'Software Architect'),
        ('DEVOPS', 'DevOps Engineer'),
        ('QA', 'QA Engineer'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERN', 'Intern'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=50, blank=True, help_text="Company Employee ID")
    avatar = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Professional Information
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='JUNIOR')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='FULL_TIME')
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    team = models.CharField(max_length=100, blank=True)
    reporting_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    start_date = models.DateField(null=True, blank=True)

    # Contact Information
    work_email = models.EmailField(blank=True)
    personal_email = models.EmailField(blank=True)
    work_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    # Social & Professional Profiles
    github_username = models.CharField(max_length=50, blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    stackoverflow_profile = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)

    # Technical Skills
    primary_skills = models.TextField(blank=True, help_text="Main technical skills (comma-separated)")
    secondary_skills = models.TextField(blank=True, help_text="Secondary technical skills (comma-separated)")
    certifications = models.TextField(blank=True, help_text="Professional certifications")
    
    # Preferences
    timezone = models.CharField(max_length=50, blank=True)
    preferred_programming_languages = models.TextField(blank=True, help_text="Preferred programming languages (comma-separated)")
    preferred_work_hours = models.CharField(max_length=100, blank=True, help_text="e.g., '9 AM - 5 PM EST'")

    # System fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # Appearance Settings
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default')
    ]
    
    CODE_THEME_CHOICES = [
        ('github', 'GitHub'),
        ('monokai', 'Monokai'),
        ('dracula', 'Dracula'),
        ('solarized', 'Solarized')
    ]
    
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='system')
    sidebar_collapsed = models.BooleanField(default=False)
    code_theme = models.CharField(max_length=20, choices=CODE_THEME_CHOICES, default='github')
    
    # Integration Settings
    github_access_token = models.CharField(max_length=255, blank=True)
    gitlab_access_token = models.CharField(max_length=255, blank=True)
    jira_access_token = models.CharField(max_length=255, blank=True)
    
    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    desktop_notifications = models.BooleanField(default=True)
    mention_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def years_of_experience(self):
        if self.start_date:
            from datetime import date
            today = date.today()
            years = today.year - self.start_date.year
            if today.month < self.start_date.month or (today.month == self.start_date.month and today.day < self.start_date.day):
                years -= 1
            return years
        return None

# Move signal handlers outside the model class
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Add attachment fields
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    attachment_type = models.CharField(max_length=20, blank=True, choices=[
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('FILE', 'File')
    ])
    attachment_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.project:
            return f"Project message in {self.project.title} by {self.sender.username}"
        return f"DM from {self.sender.username} to {self.recipient.username}"
