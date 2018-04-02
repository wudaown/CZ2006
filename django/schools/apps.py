from django.apps import AppConfig
import logging

_logger = logging.getLogger(__name__)

class SchoolsConfig(AppConfig):
    name = 'schools'
    label = 'schools'
    def ready(self):
        _logger.warning(">>'%s' completed initialisation.", self.label)
        import schools.signals

