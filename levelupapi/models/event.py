from django.db import models

class Event(models.Model):
    description = models.CharField(max_length=255)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    time = models.TimeField()
    attendees = models.ManyToManyField('Gamer', through='Attendance')
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='events')

    @property
    def joined(self):
        ''' Joining the event. '''
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
