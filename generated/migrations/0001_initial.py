# Generated by Django 4.1.5 on 2024-05-07 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import generated.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cloths', '0003_alter_userclothes_image_alter_userimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_image', models.ImageField(upload_to=generated.models.user_generated_upload_to)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_fav', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_generated_images', to=settings.AUTH_USER_MODEL)),
                ('user_clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cloth', to='cloths.userclothes')),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_image', to='cloths.userimage')),
            ],
        ),
    ]
