from django.db import models

class picture(models.Model):
    name = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    picture = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return self.name if self.name else "작가 이름이 입력되지 않았습니다."