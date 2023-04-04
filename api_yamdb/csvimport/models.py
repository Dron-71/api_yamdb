from django.db import models


class CsvImport(models.Model):
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)
