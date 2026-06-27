from dataclasses import dataclass


@dataclass
class ExecutiveCandidate:
    full_name: str
    title: str
    email: str | None
    linkedin_url: str | None
    seniority: str


class EnrichmentService:
    def enrich_executives(self, company_name: str, domain: str) -> list[ExecutiveCandidate]:
        base = company_name.split()[0] if company_name else domain.split(".")[0].title()
        return [
            ExecutiveCandidate(full_name=f"Ava {base}", title="VP of Revenue", email=None, linkedin_url=f"https://linkedin.com/in/ava-{base.lower()}", seniority="vp"),
            ExecutiveCandidate(full_name=f"Noah {base}", title="Head of Operations", email=None, linkedin_url=f"https://linkedin.com/in/noah-{base.lower()}", seniority="director"),
            ExecutiveCandidate(full_name=f"Mia {base}", title="CEO", email=None, linkedin_url=f"https://linkedin.com/in/mia-{base.lower()}", seniority="c-suite"),
        ]