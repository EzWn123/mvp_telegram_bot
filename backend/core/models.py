from django.db import models

sex = [
    ('man', 'Мужской'),
    ('woman', 'Женский'),
]

military_card = [
    ('yes', 'Да'),
    ('no', 'Нет'),
]

education = [
    ('higher', 'Высшее'),
    ('specialized_secondary', 'Среднее специальное'),
    ('average', 'Среднее'),
]

fits = [
    ('choise', 'Выберите'),
    ('yes', 'Подходит'),
    ('no', 'Не подходит'),
]


class User(models.Model):
    messenger_id = models.BigIntegerField(verbose_name='Мессенджер ID')
    surname = models.CharField(
        verbose_name='Фамилия', max_length=32, null=True, blank=True)
    name = models.CharField(
        verbose_name='Имя', max_length=32, null=True, blank=True)
    second_name = models.CharField(
        verbose_name='Отчество', max_length=32, null=True, blank=True)
    birthday = models.CharField(
        verbose_name='Дата рождения', max_length=32, null=True, blank=True)
    age = models.IntegerField(verbose_name='Возраст', null=True, blank=True)
    sex = models.CharField(verbose_name='Пол', max_length=3,
                           choices=sex, null=True, blank=True)
    nationality = models.CharField(
        verbose_name='Национальнасть', max_length=32, null=True, blank=True)
    mobile_phone = models.CharField(
        verbose_name='Мобильный телефон', max_length=32, null=True, blank=True)
    email = models.CharField(verbose_name='E-MAIL',
                             max_length=64, null=True, blank=True)
    passport_data = models.CharField(
        verbose_name='Паспортные данные', max_length=64, null=True, blank=True)
    military_card = models.CharField(
        verbose_name='Военный билет', max_length=3, choices=military_card, null=True, blank=True)
    education = models.CharField(
        verbose_name='Образование', max_length=30, choices=education, null=True, blank=True)
    fit = models.CharField(
        verbose_name='Ответ для кандидата', max_length=20, choices=fits, default='choise')
    state = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Соискатель'
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Соискатель', related_name='messages')
    text = models.TextField(verbose_name='Текст')
    from_user = models.BooleanField(
        verbose_name='От пользователя', default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return 'от {}'.format(self.user.name if self.from_user else 'оператора')
