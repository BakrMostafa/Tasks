from django.contrib import admin
from .models import Project, Task, Note, Tag, File, KnowledgeBase, UserProfile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'priority', 'status', 'due_date')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'project', 'task', 'created_at')
    list_filter = ('created_at', 'updated_at', 'project')
    search_fields = ('title', 'content')
    raw_id_fields = ('project', 'task')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'project')
    search_fields = ('name',)
    raw_id_fields = ('project',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'job_title', 'department', 'mobile_phone', 'date_joined')
    search_fields = ('user__username', 'user__email', 'job_title', 'department')
    list_filter = ('user_type', 'department', 'date_joined')