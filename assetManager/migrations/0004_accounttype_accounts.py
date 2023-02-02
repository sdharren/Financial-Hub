# Generated by Django 4.1.5 on 2023-02-01 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assetManager', '0003_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('account_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_date_linked', models.DateField(default=django.utils.timezone.now, verbose_name='Account Linked Date')),
                ('account_asset_type', models.CharField(choices=[('DEBIT', 'Debit Card'), ('CREDIT', 'Credit Card'), ('STOCK', 'Brokerage or Investement Account'), ('CRYPTO', 'Crypto Wallet')], max_length=35)),
                ('access_token', models.CharField(max_length=250)),
            ],
            options={
                'unique_together': {('account_type_id', 'access_token')},
            },
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('account_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_firm_name', models.CharField(max_length=100)),
                ('account_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_type', to='assetManager.accounttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('account_id', 'user', 'account_type_id')},
            },
        ),
    ]
