from django.db import migrations


def clear_home_showcases(apps, schema_editor):
    HomeShowcase = apps.get_model("cms", "HomeShowcase")
    HomeShowcase.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0007_strip_placeholder_cms_copy"),
    ]

    operations = [
        migrations.RunPython(clear_home_showcases, migrations.RunPython.noop),
    ]
