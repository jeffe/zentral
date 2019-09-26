# Generated by Django 2.2.3 on 2019-09-25 09:18

from django.db import migrations


def convert_probe_source(apps, schema_editor):
    ProbeSource = apps.get_model("probes", "ProbeSource")
    for ps in ProbeSource.objects.all():
        old_payload_filters = ps.body.get("filters", {}).get("payload", [])
        if not old_payload_filters:
            continue
        new_payload_filters = []
        for old_payload_filter in old_payload_filters:
            new_payload_filters.append([
                {"attribute": k,
                 "operator": v["operator"],
                 "values": v["values"]}
                for k, v in old_payload_filter.items()
            ])
        ps.body["filters"]["payload"] = new_payload_filters
        ps.save()


class Migration(migrations.Migration):

    dependencies = [
        ('probes', '0010_auto_20190925_0255'),
    ]

    operations = [
        migrations.RunPython(convert_probe_source),
    ]