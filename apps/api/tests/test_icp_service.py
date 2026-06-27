from app.services.icp_service import ICPScoringService


def test_icp_scoring_increases_with_signals() -> None:
    service = ICPScoringService()
    score, reasons = service.score("SaaS", {"open_roles": 10}, ["A", "B", "C"])
    assert score > 50
    assert reasons