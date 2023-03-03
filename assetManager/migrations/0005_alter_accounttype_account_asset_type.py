# Generated by Django 4.1.5 on 2023-03-03 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetManager', '0004_alter_accounttype_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='account_asset_type',
            field=models.CharField(blank=True, choices=[('transactions', 'Debit Card'), ('investments', 'Brokerage or Investement Account'), ('CRYPTO', 'Crypto Wallet')], max_length=35),
        ),
    ]