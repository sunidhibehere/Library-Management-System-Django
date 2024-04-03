# Generated by Django 5.0.1 on 2024-01-30 13:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('fiction', 'Fiction'), ('non-fiction', 'Non-Fiction'), ('biography', 'Biography'), ('history', 'History'), ('science', 'Science'), ('poetry', 'Poetry'), ('drama', 'Drama'), ('religion', 'Religion'), ('children', 'Children'), ('other', 'Other')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('borrowing_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('status', models.CharField(choices=[('available', 'Available'), ('borrowed', 'Borrowed')], default='available', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('amount_due', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('return_date', models.DateField()),
                ('returned', models.BooleanField(default=False)),
                ('fine', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to='library.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to='library.member')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('mpesa', 'Mpesa'), ('card', 'Card')], max_length=20)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='library.member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
