from django.apps import AppConfig
import logging

_logger = logging.getLogger(__name__)

class SchoolsConfig(AppConfig):
    name = 'schools'
    label = 'schools'
    def ready(self):
        """
            Override this method to perform initialization task of registering signals.

            Register post_save signals for updating kindergarten information.
         """
        _logger.warning(">>'%s' completed initialisation.", self.label)
        import schools.signals

