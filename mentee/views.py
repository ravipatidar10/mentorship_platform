from django.shortcuts import render
from mentor.models import Research
from mentorship.models import Mentorship

# Create your views here.
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
    mentors = Mentorship.objects.filter(mentee__user = request.user)
    
    return render(
        request, 
        'mentee/find_mentor.html', 
        {
            'role': 'mentee',
            'research_areas': research_areas
        }
    )
