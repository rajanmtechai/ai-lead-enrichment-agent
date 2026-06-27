class CRMService:
    def sync(self, provider: str, draft: dict) -> dict:
        return {
            "provider": provider,
            "status": "queued",
            "message": f"Sync to {provider} prepared for approval-gated delivery.",
            "draft_kind": draft.get("kind"),
        }