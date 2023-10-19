from django.shortcuts import render
from django.db.models import Q

from mentor.models import Research
from mentorship.models import Mentorship
from mentor.models import Mentor, ResearchDetails


def dashboard(request):
    return render(
        request,
        'mentee/dashboard.html',
        {
            'role': 'mentee',
        }
    )


def find_mentor(request):
    research_areas = Research.objects.all()
    exclude_researches = Mentorship.objects.filter(
        mentee__user=request.user).values_list("research__id", flat=True)
    researches = ResearchDetails.objects.exclude(id__in=exclude_researches)
    research_id = request.GET.get('research_id')
    if research_id:
        researches = researches.filter(research__id=research_id)
    username = request.GET.get('username')
    if username:
        researches = researches.filter(
            Q(mentor__user__username=username) | Q(
                mentor__user__first_name=username) | Q(mentor__user__last_name=username)
        )
    return render(
        request,
        'mentee/find_mentor.html',
        {
            'role': 'mentee',
            'research_areas': research_areas,
            'researches': researches,
            'username': username,
            'research_id': research_id,
        }
    )
