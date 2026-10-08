import os


class TraceManager:
    """Small optional wrapper so the app also runs without Langfuse credentials."""

    def __init__(self):
        self.enabled = bool(
            os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
        )
        self.client = None
        if self.enabled:
            try:
                from langfuse import Langfuse
                self.client = Langfuse()
            except Exception:
                self.enabled = False

    def flush(self):
        if self.client:
            self.client.flush()
