from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_active', 'name']
        verbose_name = 'entreprise'
        verbose_name_plural = 'entreprises'

    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return None


class JobManager(models.Manager):
    def active_jobs(self):
        qs = self.filter(active=True)
        qs = qs.filter(organisation__is_active=True)
        qs = qs.exclude(is_deleted=True)
        return qs


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    contract_type = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    views_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    image = models.ImageField("Image d'illustration", upload_to='jobs/image/', null=True, blank=True)

    objects = JobManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'pk': self.pk})


class ApplicationStatus(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    INTERVIEW = 'INTERVIEW', 'Entretien'
    ACCEPTED = 'ACCEPTED', 'Accepté'
    REFUSED = 'REFUSED', 'Refusé'


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job} - {self.user}"

    class Meta:
        verbose_name = 'candidature'
        verbose_name_plural = 'candidatures'
        ordering = ['-created_at']
