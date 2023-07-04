from django.db import models
from authentification.models import MyUser as User, Level


class Subject(models.Model):
    label = models.CharField(max_length=100)
    bgColor = models.CharField(default='#FF0000', null=True, blank=True, max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.label

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'bgColor': self.bgColor,
            'level': self.level.serialize(),
        }


class Classroom(models.Model):
    label = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    capacity = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.label

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'capacity': self.capacity,
            'desc': self.desc,
        }


class Schedule(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(
        Level, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    week_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"emploi du temps du {self.start_time} au {self.end_time} de {self.subject.label}"