from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Mentorship, ACCEPTED, PENDING, REJECTED
from mentor.models import ResearchDetails

@login_required(login_url='/')
def request_mentorship(request):
    research_detail_id = request.POST.get('research_detail_id')
    print(research_detail_id)
    research_detail = ResearchDetails.objects.get(id=research_detail_id)
    mentorship = Mentorship()
    mentorship.status = PENDING
    mentorship.mentor = research_detail.mentor
    mentorship.mentee = request.user.mentee
    mentorship.research = research_detail
    mentorship.save()
    return redirect('find_mentor')

@login_required(login_url='/')
def pending_requests(request):
    role = "mentor"
    try:
        request.user.mentee
        role = "mentee"
        pending_requests = Mentorship.objects.filter(
            status=PENDING, 
            mentee=request.user.mentee
        )
    except:
        pending_requests = Mentorship.objects.filter(
            status=PENDING, 
            mentor=request.user.mentor
        )
    return render(
        request,
        role+'/pending_requests.html',
        {
            'role': role,
            'pending_requests': pending_requests
        }
    )

@login_required(login_url='/')
def cancel_request(request):
    request_id = request.POST.get('request_id')
    mentorship_request = Mentorship.objects.get(id=request_id)
    try:
        request.user.mentee
        mentorship_request.delete()
    except:
        mentorship_request.status = REJECTED
        mentorship_request.save()
    return redirect('pending_requests')

@login_required(login_url='/')
def accept_request(request):
    request_id = request.POST.get('request_id')
    mentorship_request = Mentorship.objects.get(id=request_id)
    mentorship_request.status = ACCEPTED
    mentorship_request.save()
    return redirect('pending_requests')

@login_required(login_url='/')
def get_mentees(request):
    mentorships = Mentorship.objects.filter(mentor=request.user.mentor, status=ACCEPTED)
    return render(
        request,
        'mentor/my_mentees.html',
        {
            'role': 'mentor',
            'mentorships': mentorships
        }
    )

@login_required(login_url='/')
def get_mentors(request):
    mentorships = Mentorship.objects.filter(mentee=request.user.mentee, status=ACCEPTED)
    return render(
        request,
        'mentee/my_mentors.html',
        {
            'role': 'mentee',
            'mentorships': mentorships
        }
    )