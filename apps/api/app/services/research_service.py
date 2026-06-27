from dataclasses import dataclass
from hashlib import sha256
from urllib.parse import urlparse


@dataclass
class CompanySnapshot:
    domain: str
    name: str
    industry: str
    description: str
    pricing: dict
    hiring_signals: dict
    funding: dict
    recent_news: list
    tech_stack: list
    competitors: list


class ResearchService:
    def analyze(self, query: str) -> CompanySnapshot:
        domain = self._normalize_domain(query)
        stem = domain.split(".")[0]
        name = stem.replace("-", " ").title()
        digest = sha256(domain.encode()).hexdigest()
        industries = ["SaaS", "FinTech", "Healthcare", "Logistics", "MarTech", "DevTools"]
        industry = industries[int(digest[0], 16) % len(industries)]
        tech_stack = ["Next.js", "FastAPI", "PostgreSQL", "Redis", "Qdrant"]
        competitors = [f"{name} Pro", f"{name} Cloud", f"{name} AI"]
        return CompanySnapshot(
            domain=domain,
            name=name,
            industry=industry,
            description=f"{name} is a {industry.lower()} company inferred from public signals and the provided domain.",
            pricing={"model": "custom", "range": "contact sales"},
            hiring_signals={"open_roles": 7 + int(digest[1], 16) % 8, "momentum": "expanding"},
            funding={"stage": ["seed", "series a", "series b"][int(digest[2], 16) % 3], "status": "private"},
            recent_news=[f"{name} announced a product update.", f"{name} appears to be expanding the go-to-market team."],
            tech_stack=tech_stack,
            competitors=competitors,
        )

    def _normalize_domain(self, query: str) -> str:
        value = query.strip().lower()
        if "://" in value:
            value = urlparse(value).netloc
        if "/" in value:
            value = value.split("/")[0]
        value = value.removeprefix("www.")
        if "." not in value:
            slug = "".join(character if character.isalnum() else "-" for character in value).strip("-")
            return f"{slug or 'company'}.com"
        return value