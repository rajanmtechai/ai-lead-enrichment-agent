class ICPScoringService:
    def score(self, industry: str, hiring_signals: dict, competitors: list[str]) -> tuple[float, list[str]]:
        score = 35.0
        reasons: list[str] = []
        if industry in {"SaaS", "MarTech", "DevTools"}:
            score += 20
            reasons.append("Target-friendly software category")
        if hiring_signals.get("open_roles", 0) >= 8:
            score += 15
            reasons.append("Active hiring suggests growth")
        if len(competitors) >= 3:
            score += 10
            reasons.append("Competitive market indicates budget pressure")
        return min(score, 100.0), reasons