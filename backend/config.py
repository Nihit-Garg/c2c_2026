"""
config.py — Environment variable loading for the entire backend.

OWNER: Person A (backend/api/, backend/db/)
RESPONSIBILITY: Single point of truth for all config. Import `settings` everywhere;
never call os.getenv() directly in other modules.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Typed access to all environment variables with sensible defaults."""

    # ── LLM ───────────────────────────────────────────────────────────────────
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")       # "gemini" | "ollama" | "anthropic"
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # ── Supabase ──────────────────────────────────────────────────────────────
    SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str | None = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # ── GitHub (optional for Phase 1 — only needed for PR ingestion) ──────────
    GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO: str | None = os.getenv("GITHUB_REPO")          # "owner/repo"

    # ── App ───────────────────────────────────────────────────────────────────
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> None:
        """
        Raise ValueError for any critical missing config at startup.
        GitHub token is NOT required here — only needed for Phase 9 PR ingestion.
        """
        errors = []

        if self.LLM_PROVIDER == "gemini" and not self.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is required when LLM_PROVIDER=gemini")

        if not self.SUPABASE_URL:
            errors.append("SUPABASE_URL is required")

        if not self.SUPABASE_SERVICE_ROLE_KEY:
            errors.append("SUPABASE_SERVICE_ROLE_KEY is required")

        if errors:
            raise ValueError("Config errors:\n" + "\n".join(f"  - {e}" for e in errors))


settings = Settings()
