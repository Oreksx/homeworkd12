from django.db.models.signals import m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import send_mail
from news.models import Post, Category, PostCategory
from appointments.models import Appointment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
 
 
# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.posts.through)
def notify_managers_appointment(sender, instance, action, **kwargs):
    if action == "post_add":
        category = instance.posts.all()
        categoryname = ""
        users_email = []
        textpost = instance.preview()
        urlpost = instance.get_absolute_url()
        for i in category:
            categoryname = i
        user = Appointment.objects.all().filter(subscribers=categoryname)
        for i in user:
            users_email.append(i.user.email)
        html_content = render_to_string( 
            'appointment_created.html',
            {
                'category': categoryname,
                'textpost': textpost,
                'urlpost': urlpost,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Новый пост в категории: {categoryname}',
            body=textpost,
            from_email="Robotoreksx@yandex.ru",
            to=users_email,
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()











































