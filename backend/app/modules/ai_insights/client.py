import random


class AIClient:
    """Simulated AI client — returns realistic fake insights."""

    _templates = [
        "Based on your data, churn risk is increasing. Consider targeted retention campaigns for users inactive over 14 days.",
        "MRR growth has slowed by {pct}% this month. Upsell opportunities exist in your mid-tier plan cohort.",
        "Your subscriber acquisition cost is trending upward. Evaluate paid channel ROI before scaling further.",
        "Active subscriber engagement is strong. This is a good window to test a price increase on new signups.",
        "Churn is concentrated in the first 30 days. Improving onboarding flow could reduce early cancellations by up to 20%.",
    ]

    async def generate_insight(self, prompt: str) -> str:
        # TODO: replace with real OpenAI API call
        template = random.choice(self._templates)
        pct = round(random.uniform(2.0, 15.0), 1)
        return template.format(pct=pct)
