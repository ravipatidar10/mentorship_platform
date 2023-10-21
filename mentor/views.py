from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Research, ResearchDetails

# Create your views here.

@login_required(login_url='/')
def dashboard(request):
    research_areas = Research.objects.all()
    researches = ResearchDetails.objects.filter(mentor=request.user.mentor)
    return render(
        request, 
        'mentor/dashboard.html', 
        {
            'role': 'mentor', 
            'research_areas': research_areas, 
            'researches': researches
        }
    )

@login_required(login_url='/')
def add_research_area(request):
    research_id = request.POST.get("research_area")
    other = request.POST.get("other")
    details = request.POST.get("details")
    if other:
        research = Research(research_area=other)
        research.save()
    else:
        research = Research.objects.get(id=research_id)
    research_details = ResearchDetails()
    research_details.research = research
    research_details.mentor = request.user.mentor
    research_details.details = details
    research_details.save()
    return redirect('mentor_dashboard')

@login_required(login_url='/')
def delete_research_area(request):
    research_id = request.GET.get("research_id")
    ResearchDetails.objects.get(id=research_id).delete()
    return redirect('mentor_dashboard')

@login_required(login_url='/')
def update_research_area(request):
    research_details_id = request.POST.get("research_details_id")
    research_details = ResearchDetails.objects.get(id=research_details_id)
    details = request.POST.get("details")
    research_details.details = details
    research_details.save()
    return redirect('mentor_dashboard')
