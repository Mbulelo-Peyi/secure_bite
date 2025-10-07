# secure_bite/auth_providers/__init__.py
from importlib import import_module

try:
    oauth = import_module("secure_bite.auth_providers.oauth2")
except ModuleNotFoundError:
    oauth = None

__all__ = ["oauth"]
