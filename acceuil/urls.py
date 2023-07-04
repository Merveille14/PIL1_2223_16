from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('teachers', views.teacher, name="teacher"),
    path('subjects', views.subject, name="subject"),
    path('levels', views.level, name="level"),
    path('classrooms', views.classroom, name="classroom"),
    path('your-profile', views.profile, name="profile"),
    path('your-timetables/<int:pk>', views.schedule, name="timetable"),

    path('delete-shedule/<int:pk>', views.destroy_shedule, name='destroy_shedule'),
    path('your-timetables', views.students_schedule, name='timetables.students'),
]
