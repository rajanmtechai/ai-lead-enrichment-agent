class OutreachService:
    def generate(self, company_name: str, executives: list[dict], icp_score: float, buying_signals: list[str], pain_points: list[str]) -> list[dict]:
        angle = pain_points[0] if pain_points else "pipeline efficiency"
        executive_name = executives[0]["full_name"] if executives else "your team"
        executive_title = executives[0]["title"] if executives else "leadership"
        subject_lines = [
            f"A faster path to {angle}",
            f"{company_name} and {angle}",
            f"Quick idea for your team",
        ]
        drafts = [
            {
                "kind": "cold_email_sequence",
                "subject_lines": subject_lines,
                "content": {
                    "email_1": f"Hi {executive_name}, I noticed {company_name} showing signals around {angle}. We help teams turn that into a measurable pipeline lift.",
                    "email_2": f"Following up with a more concrete idea for {company_name}: use the current {buying_signals[0].lower()} to create a cleaner outreach motion for {executive_title} priorities.",
                    "email_3": f"If {angle} is a priority, I can share a short plan tailored to {company_name}.",
                },
                "notes": "Generated from ICP and buying-signal heuristics.",
            },
            {
                "kind": "linkedin_sequence",
                "subject_lines": [f"{company_name} outreach idea"],
                "content": {
                    "connect_request": f"{company_name} looks like a strong fit for a quick idea I have around {angle}.",
                    "follow_up_1": f"Thanks for connecting. I reviewed a few signals and think there is an opportunity to improve {angle} for your team.",
                },
                "notes": "Short-form LinkedIn sequence.",
            },
            {
                "kind": "call_script",
                "subject_lines": [f"{company_name} discovery call"],
                "content": {
                    "opening": f"I looked at {company_name} and wanted to verify whether {angle} is a current priority.",
                    "questions": [
                        "How are you currently measuring response quality?",
                        "Where does your team lose time in outbound research?",
                        "What would make this quarter a win for the team?",
                    ],
                    "close": "If this resonates, we can map a short pilot next.",
                },
                "notes": f"ICP score {icp_score:.1f} with focused talk track.",
            },
        ]
        return drafts