from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def index(request):
    if request.user.is_staff:
        return redirect('jobs:job_list')
    return redirect('jobs:job_list')
