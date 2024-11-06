from django.db import models


class WebServiceLog(models.Model):
    objects = models.Manager()

    created_on = models.DateTimeField(auto_now_add=True)
    headers = models.TextField()
    ip = models.CharField(max_length=50)
    payload = models.TextField()
    method = models.CharField(max_length=100)
    url = models.CharField(max_length=600)
    status_code = models.CharField(max_length=100)
    status_msg = models.CharField(max_length=100)
    response = models.TextField()

    class Meta:
        verbose_name_plural = "Web Service Logs"
        ordering = ['-created_on']

    def __str__(self):
        return self.url
