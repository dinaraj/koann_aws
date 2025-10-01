from django.contrib import admin

from jobs.models import Job, Company, JobApplication


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone'
    ]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'company',
        'name',
        'description'
    ]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'job',
        'user',
    ]
