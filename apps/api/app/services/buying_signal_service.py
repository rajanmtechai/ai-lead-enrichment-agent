class BuyingSignalService:
    def detect(self, company_name: str, hiring_signals: dict, funding: dict, recent_news: list[str]) -> list[str]:
        signals = []
        if hiring_signals.get("open_roles", 0) > 8:
            signals.append("Rapid hiring indicates team scale-up")
        if funding.get("stage") in {"series a", "series b"}:
            signals.append("Recent funding may unlock new tooling budgets")
        if recent_news:
            signals.append(f"Recent news volume for {company_name} suggests active market motion")
        return signals or ["General outreach fit with no explicit buying signal"]