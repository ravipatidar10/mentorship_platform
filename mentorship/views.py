# Python Imports
from datetime import datetime, timedelta

# 3rd Party Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import When, Case, Value, CharField

# Local Imports
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
    """
    Request for mentorship to mentor by mentee
    method type: POST
    parameters:
        research_detail_id
    """
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
    """
    Shows pending Requests
    method type: GET
    parameters:
         Request
    """
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
    """
    Handles the mentorship Cancellation Request
    method types:GET
    Parameters:
         request_id
    """
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
    """
    Accepts the mentorship Requests
    Method type:POST
    Parameters:
        request_id
    
    """
    request_id = request.POST.get('request_id')
    mentorship_request = Mentorship.objects.get(id=request_id)
    mentorship_request.status = ACCEPTED
    mentorship_request.save()
    return redirect('pending_requests')

@login_required(login_url='/')
def get_mentees(request):
    """
    retrieve and display data of mentees on mentor side
    Method type:GET
    """
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
    """
    retrieve and display data of mentors on mentee side 
    Method type:GET
    """
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
    """
    handle the retrieval of mentorships 
    Method type:GET
    Parameters:
        role
        status
    """
    
    role = request.GET.get('role')
    status = request.GET.get('status', ACCEPTED)
    if role == 'mentee':
        mentorships = Mentorship.objects.filter(mentee=request.user.mentee, status=status)
    else:
        mentorships = Mentorship.objects.filter(mentor=request.user.mentor, status=status)
    for mentorship in mentorships:
        tasks = Tasks.objects.filter(mentorship=mentorship, status=RUNNING)[:2]
        now = datetime.now()
        meetings = Meeting.objects.filter(mentorship=mentorship, is_cancelled=False, time__gte=now)[:2]
        mentorship.tasks = tasks
        mentorship.meetings = meetings
    statuses = []
    for i in MENTORSHIP_STATUSES:
        if i[0] not in [2, 6]:
            continue
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
    """
    represent the ID of the mentorship for which tasks are being retrieved 
    Method type:GET
    Parameters:
        mentorship_id
        role
        status
    """
    mentorship_id = request.GET.get('mentorship_id')
    role = request.GET.get('role')
    task_status = request.GET.get("status")
    mentorship = Mentorship.objects.get(id=mentorship_id)
    meetings = Meeting.objects.filter(mentorship=mentorship, time__gte=datetime.now()-timedelta(hours=1))
    # if int(task_status) == 2:
    #     tasks = Tasks.objects.filter(mentorship_id=mentorship_id, start_time__gte=datetime.now())
    # elif int(task_status) == 3:
    #     tasks = Tasks.objects.filter(mentorship_id=mentorship_id, start_time__lte=datetime.now(), start_time__gte=datetime.now())
    # else:
    whens = [When(status=k, then=Value(v.replace("_", " "))) for k, v in TASK_STATUSES]
    tasks = Tasks.objects.filter(mentorship=mentorship).annotate(task_status=Case(*whens, output_field=CharField()))
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
            'meetings': meetings,
            'task_statuses': statuses,
            'mentorship': mentorship,
        }
    )

@login_required(login_url='/')
def change_mentorship_status(request):
    """
    change the status for a specific mentorship
    Method type:GET
    Parameters:
        mentorship_id 
        status
    """ 
    mentorship_id = request.GET.get('mentorship_id')
    status = request.GET.get('status')
    mentorship = Mentorship.objects.get(id=mentorship_id)
    mentorship.status = status
    mentorship.save()
    return redirect('get_mentorships')

@login_required(login_url='/')
def change_task_status(request):
    """
    change of status for a specific task
    Method type:GET
    Parameters:
        task_id
        status
        role
    """ 
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
    """
    Create a new task
    Method type:GET
    Parameters:
        role
        title
        detail
        start_date
        end_date
        mentorship_id
    """ 
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

@login_required(login_url='/')
def cancel_meeting(request):
    """
    Cancel meeting
    Method type:GET
    Parameters:
        role
        meet_id
    """
    meet_id = request.GET.get('meet_id')
    role = request.GET.get('role')
    meet = Meeting.objects.get(id=meet_id)
    meet.is_cancelled = True
    meet.save()
    url = reverse('get_tasks')
    return redirect( f'{url}?role={role}&mentorship_id={meet.mentorship_id}')

@login_required(login_url='/')
def create_meeting(request):
    """
    Create a new meeting
    Method type:POST
    Parameters:
        role
        title
        link
        scheduled_date
        mentorship_id
    """ 
    role = request.POST.get('role')
    title = request.POST.get('title')
    link = request.POST.get('link')
    scheduled_date = request.POST.get('scheduled_date')
    mentorship_id = request.POST.get('mentorship_id')
    meeting = Meeting(
        title=title, 
        link=link, 
        mentorship_id=mentorship_id,
        time=scheduled_date,
    )
    meeting.save()
    url = reverse('get_tasks')
    return redirect( f'{url}?role={role}&mentorship_id={mentorship_id}')