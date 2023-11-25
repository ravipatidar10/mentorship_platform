# 3rd Party Imports
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Local Imports
from mentor.models import Research
from mentorship.models import Mentorship
from mentor.models import Mentor, ResearchDetails


@login_required(login_url='/')
def dashboard(request):
    """
     render the mentee dashboard page
     Method type=GET
    """
    return render(
        request,
        'mentee/dashboard.html',
        {
            'role': 'mentee',
        }
    )

@login_required(login_url='/')
def find_mentor(request):
    """
     search for mentors based on research areas or usernames
     Method type=GET
     Parameters:
        research_id
        username 
    """
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
    else:
        username = ""
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
