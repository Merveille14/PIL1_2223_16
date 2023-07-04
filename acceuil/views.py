from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Classroom, Subject, Schedule
from authentification.models import MyUser as User, Level
import uuid
from authentification.mail import send_html_email


def superuser_required(view_func):
    def check_user(request, *args, **kwargs):
        if not request.user.is_authenticated or (not request.user.is_superuser):
            return redirect('timetables.students')
        return view_func(request, *args, **kwargs)

    return check_user

def send_my_mail(shedule):
    student_message = f"Un nouveau emploi du temps programmé pour le {shedule.start_date}"
    teacher_message = f"Vous êtes programmé pour le {shedule.start_date} en {shedule.subject.level.label}"
    message = ''
    levelId = shedule.subject.level.id
    users = User.objects.filter(Q(id=shedule.teacher_id) | Q(level=levelId))

    for user in users:
        if user.is_teacher:
            message = teacher_message
        else:
            message = student_message

        try:
            send_html_email("Nouveau Emploi du Temps", 'mails/new-shedule.html', {
                'message': message,
                'to': user
            })
        except:
            continue

@login_required
def home(request):
    
    context = {

    }

    return render(request, 'acceuil/home.html', context)


@login_required
def profile(request):
    
    error, success = (None, None)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        level_id = request.POST.get('level_id')

        if first_name and last_name and email:
            if not User.objects.filter(email=email).exclude(id=request.user.id).count():
                user = request.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                if not request.user.is_superuser:
                    user.level = Level.objects.get(id=level_id)
                user.save()

                success = "Your account has been successfully updated"
            else:
                error = "User with the same email address already exist"
        else:
            error = "Error, It looks like somes fields are blank"

    context = {
        'levels': Level.objects.all(),
        'error': error,
        'success': success,
    }

    return render(request, 'acceuil/profile.html', context)


@login_required
@superuser_required
def subject(request):
    error, success = None, None

    levels = Level.objects.all()

    if request.method == 'POST':
        label = request.POST.get('label')
        bgColor = request.POST.get('bgColor')
        level_id = request.POST.get('level_id')
        action = request.POST.get('action')
        object_id = request.POST.get('object_id')

        if label:
            if action == "CREATE":
                Subject.objects.create(
                    label=label,
                    bgColor=bgColor,
                    level=Level.objects.get(id=level_id)
                )
            elif action == "UPDATE":
                subject = Subject.objects.filter(id=object_id)
                subject.update(
                    label=label,
                    bgColor=bgColor,
                    level=Level.objects.get(id=level_id)
                )
            success = "Create/Update successfully done"
        else:
            error = "Error, It looks like somes fields are blank"
        
        if action == "DELETE":
            Subject.objects.get(id=object_id).delete()
            error = None

    context = {
        'subjects': Subject.objects.all(),
        'levels': levels,
        'error': error,
        'success': success,
    }
    return render(request, 'acceuil/subject.html', context)

@login_required
@superuser_required
def teacher(request):
    error, success = None, None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = bool(request.POST.get('is_superuser'))
        is_teacher = bool(request.POST.get('is_teacher'))

        action = request.POST.get('action')
        object_id = request.POST.get('object_id')

        if first_name and last_name and email:

            if not User.objects.filter(email=email).exclude(id=object_id).count():
                password = f"ifri-{ uuid.uuid4().hex }"
                if action == "CREATE":                    
                    User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                        is_teacher=is_teacher,
                        is_superuser=is_superuser,
                    )
                elif action == "UPDATE":
                    user = User.objects.get(id=object_id)

                    user.first_name=first_name
                    user.last_name=last_name
                    user.email=email
                    user.set_password(password)
                    user.is_teacher=is_teacher
                    user.is_superuser=is_superuser
                    user.save()
                success = f"Create/Update successfully done with password <span class='d-block fs-2 text-center text-danger'> {password} </span> "
            else:
                error = "User with the same email address already exist"
        else:
            error = "Error, It looks like somes fields are blank"
        
        if action == "DELETE":
            User.objects.get(id=object_id).delete()
            error = None

    context = {
        'users': User.objects.filter(Q(is_teacher=True) | Q(is_superuser=True)).exclude(email=request.user.email),
        'error': error,
        'success': success,
    }
    return render(request, 'acceuil/teacher.html', context)

@superuser_required
@login_required
def level(request):
    error, success = None, None

    if request.method == 'POST':
        label = request.POST.get('label')
        capacity = request.POST.get('capacity')

        action = request.POST.get('action')
        object_id = request.POST.get('object_id')

        if label:
            if action == "CREATE":
                Level.objects.create(
                    label=label,
                    capacity=capacity,
                )
            elif action == "UPDATE":
                level = Level.objects.filter(id=object_id)
                level.update(
                    label=label,
                    capacity=capacity,
                )
            success = "Create/Update successfully done"
        else:
            error = "Error, It looks like somes fields are blank"
        
        if action == "DELETE":
            Level.objects.get(id=object_id).delete()
            error = None

    context = {
        'levels': Level.objects.all(),
        'error': error,
        'success': success,
    }
    return render(request, 'acceuil/level.html', context)

@superuser_required
@login_required
def classroom(request):
    error, success = None, None

    if request.method == 'POST':
        label = request.POST.get('label')
        capacity = request.POST.get('capacity')
        desc = request.POST.get('desc')

        action = request.POST.get('action')
        object_id = request.POST.get('object_id')

        if label:
            if action == "CREATE":
                Classroom.objects.create(
                    label=label,
                    capacity=capacity,
                    desc=desc,
                )
            elif action == "UPDATE":
                classroom = Classroom.objects.filter(id=object_id)
                classroom.update(
                    label=label,
                    capacity=capacity,
                    desc=desc,
                )
            success = "Create/Update successfully done"
        else:
            error = "Error, It looks like somes fields are blank"
        
        if action == "DELETE":
            Classroom.objects.get(id=object_id).delete()
            error = None

    context = {
        'classrooms': Classroom.objects.all(),
        'error': error,
        'success': success,
    }
    return render(request, 'acceuil/classroom.html', context)

@superuser_required
@login_required
def schedule(request, pk):

    try:
        current_level = Level.objects.get(id=pk)
    except:
        current_level = Level.objects.first()
        pk = current_level.id

    error, success = (None, None)

    teachers = User.objects.filter(is_teacher=True)
    subjects = Subject.objects.filter(level_id=pk)

    current_week = datetime.now().isocalendar()[1]
    current_week = int(request.GET.get('week', current_week))

    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        subject_id = request.POST.get('subject_id')
        classroom_id = request.POST.get('classroom_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if teacher_id and subject_id and pk and start_time and end_time and classroom_id:
            date = datetime.fromisoformat(start_time)
            weekNum = date.isocalendar()[1]

            try:
                shedule = Schedule.objects.create(
                    teacher=User.objects.get(id=teacher_id),
                    subject=Subject.objects.get(id=subject_id),
                    classroom=Classroom.objects.get(id=classroom_id),
                    level=Level.objects.get(id=pk),
                    start_time=start_time,
                    end_time=end_time,
                    week_num=weekNum,
                )
                send_my_mail(shedule)
            except:
                error = "Error during creating your schedule"

            success = "New Schedule created successfuly"
        else:
           "Error, It looks like somes fields are blank"

    timetable_data = get_timetable_data(pk, current_week)

    context = {
        'levels': Level.objects.all(),
        'classrooms': Classroom.objects.all(),
        'level': current_level,
        'teachers': teachers,
        'subjects': subjects,
        'errors': error,
        'success': success,
        'timetable_data': timetable_data[0],
        'all_week': timetable_data[1],
        'current_week': current_week,
    }

    return render(request, 'acceuil/schedule.html', context)

@login_required
def students_schedule(request):
    current_week = datetime.now().isocalendar()[1]
    current_week = int(request.GET.get('week', current_week))
    timetable_data = get_timetable_data(
        request.user.level.id, current_week)

    context = {
        'timetable_data': timetable_data[0],
        'all_week': timetable_data[1],
        'current_week': current_week,
        'level': request.user.level,
    }

    return render(request, 'acceuil/schedule.html', context)

@superuser_required
@login_required
def destroy_shedule(request, pk):
    next = request.GET.get('next')

    if not request.user.is_superuser:
        return redirect('timetables.students')

    Schedule.objects.get(id=pk).delete()

    return redirect(next)


def get_hour_range(time):
    hour = time.hour

    if 0 <= hour < 10:
        return 1
    elif 10 <= hour < 13:
        return 2
    elif 13 <= hour < 16:
        return 3
    elif 16 <= hour < 24:
        return 4


def get_timetable_data(level_id, week):

    timetable_entries = Schedule.objects.filter(
            level_id=level_id, week_num=week)
            
    timetable_all = Schedule.objects.filter(
            level_id=level_id)
    
    all_week = []

    for entry in timetable_all:
        week_number = entry.start_time.isocalendar()[1]

        if week_number not in all_week:
            all_week.append(week_number)

    grouped_timetable = {}

    for entry in timetable_entries:
        week_number = entry.start_time.isocalendar()[1]
        day_name = entry.start_time.strftime('%A')

        if week_number not in grouped_timetable:
            grouped_timetable[week_number] = {}

        if day_name not in grouped_timetable[week_number]:
            grouped_timetable[week_number][day_name] = {
                1: [],
                2: [],
                3: [],
                4: [],
            }

        hour_range = get_hour_range(entry.start_time.time())

        grouped_timetable[week_number][day_name][hour_range].append({
            'id': entry.id,
            'subject': entry.subject.serialize(),
            'teacher': entry.teacher.serialize(),
            'level': entry.level.serialize(),
            'classroom': entry.classroom.serialize(),
            'start_time': str(entry.start_time.strftime("%d/%m/%Y, %H:%M")),
            'end_time': str(entry.end_time.strftime("%d/%m/%Y, %H:%M")),
        })

    timetable_data = []

    days_of_week = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day_index = datetime.now().weekday()

    for i in range(7):
        day_index = (current_day_index + i) % 7
        day_name = days_of_week[day_index]
        day_data = {
            'day_name': day_name.capitalize(),
            'time_slots': {},
        }

        for hour_range in range(1, 5):
            hour_range_data = grouped_timetable.get(
                week, {}).get(day_name, {}).get(hour_range, [])
            day_data['time_slots'][hour_range] = hour_range_data

        timetable_data.append(day_data)

    return [timetable_data, all_week]
