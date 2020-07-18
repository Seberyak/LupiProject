from django.db import models


class Posts(models.Model):
    # id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ", " + str(self.name)


class Routes(models.Model):
    url_main_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    url_destination_id = models.IntegerField()
    ancestors = models.CharField(max_length=255)

    def __str__(self):
        return str(self.url_main_id) + ', ' + str(self.url_destination_id) + ',' + str(self.route)
