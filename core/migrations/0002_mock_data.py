from django.db import migrations

def create_mock_data(apps, schema_editor):
    User = apps.get_model("core", "User")
    Post = apps.get_model("core", "Post")
    Comment = apps.get_model("core", "Comment")

    user1 = User.objects.create(username="user1", email="user1@example.com")
    user2 = User.objects.create(username="user2", email="user2@example.com")

    post1 = Post.objects.create(author=user1, content="Первый тестовый пост")
    post2 = Post.objects.create(author=user2, content="Второй тестовый пост")

    Comment.objects.create(author=user2, post=post1, content="Комментарий 1")
    Comment.objects.create(author=user1, post=post2, content="Комментарий 2")

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),  # Зависимость от первой миграции
    ]

    operations = [
        migrations.RunPython(create_mock_data),
    ]
