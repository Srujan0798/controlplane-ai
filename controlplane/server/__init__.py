"""ControlPlane HTTP surface — OpenAI-compatible proxy + judge APIs + console."""
from controlplane.server.app import create_app

__all__ = ["create_app"]
