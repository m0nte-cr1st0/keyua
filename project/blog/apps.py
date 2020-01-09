from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'project.blog'

    def ready(self):
        import project.blog.signals