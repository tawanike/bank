from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    users = [
        {
            'first_name': 'Ford ',
            'last_name': 'Zephyr',
            'username': 'ford.zephyr@gmail.com',
            'email': 'ford.zephyr@gmail.com',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'first_name': 'Aiden',
            'last_name': 'Diggede',
            'username': 'diggede@consul.com',
            'email': 'diggede@consul.com',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'first_name': 'Allan',
            'last_name': 'Hardy',
            'username': 'allan.hardy@angila.com',
            'email': 'allan.hardy@angila.com', 
            'is_staff': False,
            'is_superuser': False,
        }
    ]

    for user in users:
        User.objects.create(
            username=user.get('username'),
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            email=user.get('email'),
            password=make_password('password'),
            is_staff=user.get('is_staff'),
            is_superuser=user.get('is_superuser')
        )

def reverse_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.all().delete()


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_users, reverse_func)
    ]