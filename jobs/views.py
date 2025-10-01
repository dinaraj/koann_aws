from django.db import models
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import Job


def job_list(request):
    """
    Liste des offres actives (et entreprises actives), triées par date de publication puis création.
    Recherche full-text simple via ?q=
    Pagination 10 items/page.
    """
    qs = (
        Job.objects.filter(is_active=True, company__is_active=True)
        .exclude(date_end__lt=timezone.now().date())
        .select_related("company")
        .order_by("-published_at", "-created_at")
    )

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(place__icontains=q)
            | Q(company__name__icontains=q)
        )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)

    context = {"jobs": jobs, "q": q}
    return render(request, "jobs/job_list.html", context)


def job_detail(request, pk):
    """
    Détail d’une offre. Incrémente le compteur de vues (best-effort).
    """
    job = get_object_or_404(
        Job.objects.select_related("company"),
        pk=pk,
        is_active=True,
        company__is_active=True,
    )

    # Incrément "soft" du compteur
    Job.objects.filter(pk=job.pk).update(views_number=models.F("views_number") + 1)
    job.views_number += 1  # pour l'affichage immédiat

    context = {"job": job}
    return render(request, "jobs/job_detail.html", context)
