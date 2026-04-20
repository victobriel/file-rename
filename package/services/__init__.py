"""Application services that orchestrate the domain model and infrastructure.

Still Qt-free: callers pass ``on_progress`` / ``label_provider`` callables so
the view layer can listen without leaking widgets into the services.
"""
