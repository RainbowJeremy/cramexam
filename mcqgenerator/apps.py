from django.apps import AppConfig


class McqgeneratorConfig(AppConfig):
    name = 'mcqgenerator'

    def ready(self):
        import mcqgenerator.signals
