# app/agents/coordinator.py
import time

from groq import Groq, GroqError, RateLimitError
from app.config import settings
from app.agents.prompts import (
    FIT_ANALYST_PROMPT, RESUME_WRITER_PROMPT,
    COVER_LETTER_PROMPT, INTERVIEWER_PROMPT,
    ATS_SCORER_PROMPT
)

class AgentCoordinator:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.max_retries = settings.GROQ_MAX_RETRIES

    def _call_llm(self, system_prompt: str, user_content: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content
            except RateLimitError as e:
                if attempt >= self.max_retries:
                    raise
                # If the limit is daily/token-based, retrying is unlikely to help.
                if "per day" in str(e).lower() or "tokens per day" in str(e).lower():
                    raise
                time.sleep(2 ** attempt)
            except GroqError as e:
                raise RuntimeError(f"Groq API error: {e}") from e
            except Exception as e:
                raise RuntimeError(f"LLM request failed: {e}") from e

    def analyze_fit(self, resume_text: str, jd_text: str) -> str:
        prompt_input = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
        return self._call_llm(FIT_ANALYST_PROMPT, prompt_input)

    def rewrite_resume(self, resume_text: str, jd_text: str, fit_analysis: str | None = None) -> str:
        prompt_input = f"RESUME:\n{resume_text}\n\nJD:\n{jd_text}"
        if fit_analysis:
            prompt_input += f"\n\nFIT_ANALYSIS:\n{fit_analysis}"
        return self._call_llm(RESUME_WRITER_PROMPT, prompt_input)

    def write_cover_letter(self, resume_text: str, jd_text: str, fit_analysis: str | None = None, resume_rewrite: str | None = None) -> str:
        prompt_input = f"RESUME:\n{resume_text}\n\nJD:\n{jd_text}"
        if fit_analysis:
            prompt_input += f"\n\nFIT_ANALYSIS:\n{fit_analysis}"
        if resume_rewrite:
            prompt_input += f"\n\nTAILORED_RESUME:\n{resume_rewrite}"
        return self._call_llm(COVER_LETTER_PROMPT, prompt_input)

    def create_interview_qa(self, resume_rewrite: str, jd_text: str) -> str:
        prompt_input = f"TAILORED_RESUME:\n{resume_rewrite}\n\nJD:\n{jd_text}"
        return self._call_llm(INTERVIEWER_PROMPT, prompt_input)

    def score_ats(self, resume_rewrite: str, jd_text: str) -> str:
        prompt_input = f"TAILORED_RESUME:\n{resume_rewrite}\n\nJD:\n{jd_text}"
        return self._call_llm(ATS_SCORER_PROMPT, prompt_input)

    def run_pipeline(self, resume_text: str, jd_text: str) -> dict:
        fit_analysis = self.analyze_fit(resume_text, jd_text)
        resume_rewrite = self.rewrite_resume(resume_text, jd_text, fit_analysis)
        cover_letter = self.write_cover_letter(resume_text, jd_text, fit_analysis, resume_rewrite)
        interview_qa = self.create_interview_qa(resume_rewrite, jd_text)
        ats_score = self.score_ats(resume_rewrite, jd_text)
        return {
            "fit_analysis": fit_analysis,
            "resume_rewrite": resume_rewrite,
            "cover_letter": cover_letter,
            "interview_qa": interview_qa,
            "ats_score": ats_score
        }

    def regenerate_section(self, section: str, resume_text: str, jd_text: str, fit_analysis: str | None = None, resume_rewrite: str | None = None) -> str:
        section = section.lower()
        if section == "fit_analysis":
            return self.analyze_fit(resume_text, jd_text)
        if section == "resume_rewrite":
            return self.rewrite_resume(resume_text, jd_text, fit_analysis)
        if section == "cover_letter":
            return self.write_cover_letter(resume_text, jd_text, fit_analysis, resume_rewrite)
        if section == "interview_qa":
            if not resume_rewrite:
                raise ValueError("Resume rewrite is required to regenerate interview questions")
            return self.create_interview_qa(resume_rewrite, jd_text)
        if section == "ats_score":
            if not resume_rewrite:
                raise ValueError("Resume rewrite is required to regenerate ATS score")
            return self.score_ats(resume_rewrite, jd_text)
        raise ValueError(f"Unknown regeneration section: {section}")