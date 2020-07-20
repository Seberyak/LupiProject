from django.db import models


class Posts(models.Model):
    # id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ", " + str(self.name)


class Routes(models.Model):

    main_id = models.IntegerField(default=0)
    destination_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.main_id) + ', ' + str(self.destination_id)
