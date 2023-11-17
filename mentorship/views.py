from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import When, Case, Value, CharField

from .models import (
    Mentorship, 
    Meeting,
    Tasks,
    ACCEPTED, 
    PENDING, 
    REJECTED, 
    MENTORSHIP_STATUSES,
    TASK_STATUSES,
    RUNNING,
)
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

@login_required(login_url='/')
def get_mentorships(request):
    role = request.GET.get('role')
    status = request.GET.get('status', ACCEPTED)
    if role == 'mentee':
        mentorships = Mentorship.objects.filter(mentee=request.user.mentee, status=status)
    else:
        mentorships = Mentorship.objects.filter(mentor=request.user.mentor, status=status)
    statuses = []
    for i in MENTORSHIP_STATUSES:
        if int(i[0]) == int(status):
            statuses.append({'key': i[0], 'val': i[1], 'selected': True})
        else:
            statuses.append({'key': i[0], 'val': i[1], 'selected': False})

    return render(
        request,
        'mentorship/mentorships.html',
        {
            'role': role,
            'mentorships': mentorships,
            'status': status,
            'statuses': statuses,
        }
    )
    
@login_required(login_url='/')
def get_tasks(request):
    mentorship_id = request.GET.get('mentorship_id')
    role = request.GET.get('role')
    task_status = request.GET.get("status")
    meetings = Meeting.objects.filter(mentorship_id=mentorship_id)
    # if int(task_status) == 2:
    #     tasks = Tasks.objects.filter(mentorship_id=mentorship_id, start_time__gte=datetime.now())
    # elif int(task_status) == 3:
    #     tasks = Tasks.objects.filter(mentorship_id=mentorship_id, start_time__lte=datetime.now(), start_time__gte=datetime.now())
    # else:
    whens = [When(status=k, then=Value(v.replace("_", " "))) for k, v in TASK_STATUSES]
    tasks = Tasks.objects.filter(mentorship_id=mentorship_id).annotate(task_status=Case(*whens, output_field=CharField()))
    if task_status:
        tasks = tasks.filter(status=task_status)

    print(tasks)
    statuses = []
    for i in TASK_STATUSES:
        if str(i[0]) == str(task_status):
            statuses.append({'key': i[0], 'val': i[1].replace('_', ' '), 'selected': True})
        else:
            statuses.append({'key': i[0], 'val': i[1].replace('_', ' '), 'selected': False})
    return render(
        request,
        'mentorship/tasks.html',
        {
            'role': role,
            'tasks': tasks,
            'meeting': meetings,
            'task_statuses': statuses,
            'mentorship_id': mentorship_id,
        }
    )

@login_required(login_url='/')
def change_mentorship_status(request):
    mentorship_id = request.GET.get('mentorship_id')
    status = request.GET.get('status')
    mentorship = Mentorship.objects.get(id=mentorship_id)
    mentorship.status = status
    mentorship.save()
    return redirect('get_mentorships')

@login_required(login_url='/')
def change_task_status(request):
    task_id = request.GET.get('task_id')
    status = request.GET.get('status')
    role = request.GET.get('role')
    task = Tasks.objects.get(id=task_id)
    task.status = status
    task.save()
    url = reverse('get_tasks')
    return redirect( f'{url}?role={role}&mentorship_id={task.mentorship_id}')
    # return redirect('get_tasks')

@login_required(login_url='/')
def create_task(request):
    role = request.POST.get('role')
    title = request.POST.get('title')
    detail = request.POST.get('detail')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    mentorship_id = request.POST.get('mentorship_id')
    task = Tasks(
        title=title, 
        detail=detail, 
        mentorship_id=mentorship_id,
        start_time=start_date,
        end_time=end_date
    )
    task.save()
    url = reverse('get_tasks')
    return redirect( f'{url}?role={role}&mentorship_id={mentorship_id}')