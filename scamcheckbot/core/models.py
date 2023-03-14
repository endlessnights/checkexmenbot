from django.db import models


# Create your models here.

class Profiles(models.Model):
    userid = models.PositiveIntegerField(verbose_name='ID пользователя', null=False, unique=True)
    username = models.CharField(verbose_name='TG Username', blank=True, max_length=100)
    regdate = models.DateField(verbose_name='Дата регистрации', null=False, auto_now_add=True)
    usedate = models.DateField(verbose_name='Последнее использование', null=False, auto_now=True)

    def __str__(self):
        return self.username

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'


class Scammers(models.Model):
    name = models.CharField(verbose_name='Имя мошенника', max_length=100, blank=False)
    taxid = models.PositiveIntegerField(verbose_name='ИИН', null=True, blank=True)
    added = models.DateField('Дата добавления', null=False, auto_now_add=True)
    update = models.DateField('Дата обновления данных', null=False, auto_now=True)
    checkcount = models.PositiveIntegerField('Кол-во запросов', default=0, null=False)
    fraudcount = models.PositiveIntegerField('Кол-во обманутых', default=0, null=False)
    fraudsum = models.PositiveIntegerField('Сколько денег потеряно', default=0, null=False)
    comment = models.TextField(verbose_name='Описание деятельности', blank=True, max_length=1000)
    photo = models.ImageField(upload_to='scammers/photos/', verbose_name='Фото мошенника', max_length=250, blank=True)

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'мошенник'
        verbose_name_plural = 'мошенники'


class Scammersdata(models.Model):
    scammer = models.ForeignKey(Scammers, verbose_name='Мошенник', on_delete=models.CASCADE)
    tel = models.CharField(verbose_name='Номер телефона', blank=True, max_length=20)
    tg = models.CharField(verbose_name='Telegram @username', blank=True, max_length=40)
    card = models.CharField(verbose_name='Номер карты', blank=True, max_length=20)

    def __str__(self):
        return str(self.scammer)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'данные мошенников'
        verbose_name_plural = 'данные мошенников'
