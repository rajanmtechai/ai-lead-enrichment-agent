from app.services.outreach_service import OutreachService


def test_outreach_generation_returns_sequences() -> None:
    service = OutreachService()
    drafts = service.generate("Acme", [{"full_name": "Ava Acme"}], 72.0, ["signal"], ["pipeline quality"])
    assert len(drafts) == 3
    assert drafts[0]["kind"] == "cold_email_sequence"