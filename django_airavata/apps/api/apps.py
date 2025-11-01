from django.apps import AppConfig
try:
    # Try importlib.metadata first (Python 3.10+)
    from importlib.metadata import entry_points
    def iter_entry_points(group):
        """Wrapper for compatibility with pkg_resources API"""
        eps = entry_points()
        if hasattr(eps, 'select'):
            # Python 3.10+
            return eps.select(group=group)
        else:
            # Python 3.9
            return eps.get(group, [])
except ImportError:
    # Fallback to pkg_resources for older Python versions
    from pkg_resources import iter_entry_points


class ApiConfig(AppConfig):
    name = 'django_airavata.apps.api'
    label = 'django_airavata_api'

    def ready(self):
        from . import signals  # noqa
        from . import output_views

        # Load and create instances of each output view provider
        for entry_point in iter_entry_points(group='airavata.output_view_providers'):
            output_views.OUTPUT_VIEW_PROVIDERS[entry_point.name] = entry_point.load()()
