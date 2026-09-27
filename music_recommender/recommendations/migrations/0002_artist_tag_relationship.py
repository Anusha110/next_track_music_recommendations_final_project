from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recommendations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musicbrainzartisttag",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="musicbrainzartisttag",
            name="tag_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="musicbrainzartisttag",
            constraint=models.UniqueConstraint(
                fields=("artist", "tag_id"),
                name="unique_musicbrainz_artist_tag",
            ),
        ),
    ]
