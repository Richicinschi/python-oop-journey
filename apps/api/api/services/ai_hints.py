"""AI-powered hint service using OpenAI/Claude APIs.

This service provides contextual hints, error explanations, and code reviews
using AI models while ensuring safety and cost optimization.
"""

import hashlib
import json
import logging
import os
import re
from typing import Optional

import httpx
from api.config import get_settings
from api.prompts.hints import (
    HintLevel,
    get_code_review_prompt,
    get_error_explanation_prompt,
    get_hint_prompt,
    get_safety_check_prompt,
)
from api.schemas.ai_hints import (
    AIErrorExplanation,
    AIHint,
    AIHintRequest,
    CodeReviewRequest,
    CodeReviewResult,
)

logger = logging.getLogger(__name__)


class AIHintService:
    """Service for generating AI-powered hints and code assistance."""

    # Model selection based on task complexity
    HINT_MODEL = "gpt-4o-mini"  # Cheaper model for simple hints
    ERROR_MODEL = "gpt-4o-mini"  # Cheaper model for error explanations
    REVIEW_MODEL = "gpt-4o"  # Better model for complex code reviews

    # Rate limiting and caching
    MAX_HINT_LENGTH = 200  # Max tokens for hint responses
    CACHE_TTL_HOURS = 24

    def __init__(self):
        """Initialize the AI hint service."""
        settings = get_settings()
        self.openai_api_key = getattr(settings, "openai_api_key", None) or os.getenv(
            "OPENAI_API_KEY"
        )
        self.anthropic_api_key = getattr(settings, "anthropic_api_key", None) or os.getenv(
            "ANTHROPIC_API_KEY"
        )
        self.hint_model = getattr(settings, "ai_hint_model", None) or os.getenv(
            "AI_HINT_MODEL", self.HINT_MODEL
        )
        self.review_model = getattr(settings, "ai_review_model", None) or os.getenv(
            "AI_REVIEW_MODEL", self.REVIEW_MODEL
        )

        # Simple in-memory cache (use Redis in production)
        self._cache: dict[str, dict] = {}

    def _get_cache_key(self, prefix: str, *args) -> str:
        """Generate a cache key from arguments."""
        content = json.dumps(args, sort_keys=True)
        return f"{prefix}:{hashlib.sha256(content.encode()).hexdigest()[:16]}"

    def _get_from_cache(self, key: str) -> Optional[dict]:
        """Get cached result if available."""
        return self._cache.get(key)

    def _set_cache(self, key: str, value: dict) -> None:
        """Cache a result."""
        # Simple cache - in production, use Redis with TTL
        self._cache[key] = value
        # Limit cache size
        if len(self._cache) > 1000:
            # Remove oldest entries (simple FIFO)
            oldest_keys = list(self._cache.keys())[:100]
            for k in oldest_keys:
                del self._cache[k]

    async def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        max_tokens: int = 200,
        temperature: float = 0.7,
    ) -> str:
        """Call OpenAI API.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message
            model: Model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If API call fails or no API key configured
        """
        if not self.openai_api_key:
            raise RuntimeError("OpenAI API key not configured")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                logger.error(f"OpenAI API error: {e.response.status_code} - {e.response.text}")
                raise RuntimeError(f"AI service error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"OpenAI API call failed: {e}")
                raise RuntimeError(f"AI service unavailable: {str(e)}")

    async def _call_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "claude-3-haiku-20240307",
        max_tokens: int = 200,
        temperature: float = 0.7,
    ) -> str:
        """Call Anthropic Claude API.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message
            model: Model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        if not self.anthropic_api_key:
            raise RuntimeError("Anthropic API key not configured")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["content"][0]["text"]
            except httpx.HTTPStatusError as e:
                logger.error(f"Anthropic API error: {e.response.status_code} - {e.response.text}")
                raise RuntimeError(f"AI service error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Anthropic API call failed: {e}")
                raise RuntimeError(f"AI service unavailable: {str(e)}")

    async def _is_content_safe(self, content: str) -> tuple[bool, str]:
        """Check if content is safe to process.
        
        Args:
            content: Content to check
            
        Returns:
            Tuple of (is_safe, reason)
        """
        # Simple keyword-based checks (fast path)
        unsafe_patterns = [
            r"ignore\s+(previous|earlier|above)\s+instructions",
            r"developer\s+mode",
            r"DAN\s+mode",
            r"jailbreak",
            r"ignore\s+system\s+prompt",
        ]
        
        content_lower = content.lower()
        for pattern in unsafe_patterns:
            if re.search(pattern, content_lower):
                return False, "Potential prompt injection detected"
        
        # For production, implement full AI-based safety check
        # system_prompt, user_prompt = get_safety_check_prompt(content)
        # response = await self._call_openai(system_prompt, user_prompt, self.HINT_MODEL, max_tokens=100)
        # result = json.loads(response)
        # return result.get("is_safe", True), result.get("reason", "")
        
        return True, ""

    def _extract_relevant_lines(self, code: str, hint_text: str) -> list[int]:
        """Extract line numbers referenced in the hint.
        
        Args:
            code: User's code
            hint_text: Generated hint text
            
        Returns:
            List of line numbers mentioned in the hint
        """
        lines = []
        # Look for line number references in the hint
        patterns = [
            r"line\s+(\d+)",
            r"line\s*#?(\d+)",
            r"on\s+(\d+):",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, hint_text, re.IGNORECASE)
            for match in matches:
                try:
                    line_num = int(match)
                    if 1 <= line_num <= len(code.split("\n")):
                        lines.append(line_num)
                except ValueError:
                    continue
        
        # Remove duplicates and sort
        return sorted(set(lines))

    async def generate_hint(
        self,
        problem_slug: str,
        problem_title: str,
        problem_description: str,
        user_code: str,
        hint_level: int,
        test_results: Optional[dict] = None,
        previous_hints: Optional[list[str]] = None,
    ) -> AIHint:
        """Generate a contextual hint for the user.
        
        Args:
            problem_slug: Problem identifier
            problem_title: Problem title
            problem_description: Problem description
            user_code: User's current code
            hint_level: Hint level (1-3)
            test_results: Optional test results
            previous_hints: List of previously shown hints
            
        Returns:
            AIHint with generated hint and metadata
        """
        # Validate inputs
        if not user_code or not user_code.strip():
            return AIHint(
                hint="It looks like you haven't written any code yet. Start by creating a function or class to solve the problem!",
                relevant_lines=[],
                explanation="Encouragement to start coding",
                hint_level=hint_level,
            )

        # Safety check
        is_safe, reason = await self._is_content_safe(user_code)
        if not is_safe:
            logger.warning(f"Unsafe content detected: {reason}")
            return AIHint(
                hint="I'm unable to provide hints for this code. Please focus on solving the problem using standard Python programming.",
                relevant_lines=[],
                explanation="Content safety check failed",
                hint_level=hint_level,
            )

        # Check cache
        cache_key = self._get_cache_key(
            "hint", problem_slug, user_code, hint_level, str(previous_hints)
        )
        cached = self._get_from_cache(cache_key)
        if cached:
            logger.debug("Returning cached hint")
            return AIHint(**cached)

        # Convert hint level
        try:
            level = HintLevel(hint_level)
        except ValueError:
            level = HintLevel.CONCEPTUAL

        # Get prompts
        system_prompt, user_prompt = get_hint_prompt(
            hint_level=level,
            problem_title=problem_title,
            problem_description=problem_description,
            user_code=user_code,
            test_results=test_results,
            previous_hints=previous_hints,
        )

        # Call AI
        try:
            response = await self._call_openai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=self.hint_model,
                max_tokens=self.MAX_HINT_LENGTH,
                temperature=0.7,
            )
        except RuntimeError as e:
            logger.error(f"AI hint generation failed: {e}")
            # Fallback hint
            return AIHint(
                hint="I'm having trouble connecting to my hint system right now. Try breaking the problem into smaller steps or check the documentation for guidance.",
                relevant_lines=[],
                explanation="Fallback hint due to service error",
                hint_level=hint_level,
            )

        # Extract relevant lines
        relevant_lines = self._extract_relevant_lines(user_code, response)

        # Create result
        result = AIHint(
            hint=response.strip(),
            relevant_lines=relevant_lines,
            explanation=f"Level {hint_level} hint for {problem_slug}",
            hint_level=hint_level,
        )

        # Cache result
        self._set_cache(cache_key, result.model_dump())

        # Log interaction for review
        logger.info(
            f"AI hint generated",
            extra={
                "problem_slug": problem_slug,
                "hint_level": hint_level,
                "cache_hit": False,
            },
        )

        return result

    async def explain_error(
        self,
        error_message: str,
        user_code: str,
        problem_slug: Optional[str] = None,
        problem_description: Optional[str] = None,
    ) -> AIErrorExplanation:
        """Explain an error in plain English.
        
        Args:
            error_message: The error message to explain
            user_code: User's code
            problem_slug: Optional problem identifier
            problem_description: Optional problem description
            
        Returns:
            AIErrorExplanation with explanation and suggestion
        """
        if not error_message:
            return AIErrorExplanation(
                explanation="No error message provided.",
                suggestion="Run your code to see if there are any errors.",
                relevant_lines=[],
            )

        # Safety check
        is_safe, reason = await self._is_content_safe(error_message + user_code)
        if not is_safe:
            return AIErrorExplanation(
                explanation="I'm unable to explain this error.",
                suggestion="Please focus on solving the problem using standard Python programming.",
                relevant_lines=[],
            )

        # Check cache
        cache_key = self._get_cache_key("error", error_message, user_code)
        cached = self._get_from_cache(cache_key)
        if cached:
            return AIErrorExplanation(**cached)

        # Get prompts
        system_prompt, user_prompt = get_error_explanation_prompt(
            error_message=error_message,
            user_code=user_code,
            problem_description=problem_description or "",
        )

        # Call AI
        try:
            response = await self._call_openai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=self.ERROR_MODEL,
                max_tokens=300,
                temperature=0.5,
            )
        except RuntimeError as e:
            logger.error(f"AI error explanation failed: {e}")
            return AIErrorExplanation(
                explanation=f"Error: {error_message[:100]}...",
                suggestion="Check the error message above and look for line numbers indicating where the issue occurred.",
                relevant_lines=[],
            )

        # Parse response
        explanation = response.strip()
        suggestion = ""

        # Try to extract suggestion section
        if "**How to fix it:**" in explanation:
            parts = explanation.split("**How to fix it:**")
            if len(parts) > 1:
                explanation = parts[0].replace("**What's happening:**", "").strip()
                suggestion_parts = parts[1].split("**Learning tip:**")
                suggestion = suggestion_parts[0].strip()

        # Extract relevant lines
        relevant_lines = self._extract_relevant_lines(user_code, response)

        result = AIErrorExplanation(
            explanation=explanation,
            suggestion=suggestion or "Review the error message and your code carefully.",
            relevant_lines=relevant_lines,
        )

        # Cache result
        self._set_cache(cache_key, result.model_dump())

        return result

    async def review_code(
        self,
        project_slug: str,
        project_description: str,
        files: dict[str, str],
        rubric: Optional[list[dict]] = None,
    ) -> CodeReviewResult:
        """Review code for a project submission.
        
        Args:
            project_slug: Project identifier
            project_description: Project description
            files: Dictionary of file paths to content
            rubric: Optional rubric criteria
            
        Returns:
            CodeReviewResult with review feedback
        """
        if not files:
            return CodeReviewResult(
                overall_feedback="No code submitted for review.",
                strengths=[],
                improvements=["Please submit your code files for review."],
                rubric_assessment={},
                encouragement="Ready to review when you are!",
            )

        # Safety check
        all_code = "\n".join(files.values())
        is_safe, reason = await self._is_content_safe(all_code)
        if not is_safe:
            return CodeReviewResult(
                overall_feedback="Unable to review this submission.",
                strengths=[],
                improvements=["Please ensure your code follows the assignment guidelines."],
                rubric_assessment={},
                encouragement="Focus on solving the problem using standard Python programming.",
            )

        # Get prompts
        system_prompt, user_prompt = get_code_review_prompt(
            project_slug=project_slug,
            project_description=project_description,
            files=files,
            rubric=rubric,
        )

        # Call AI
        try:
            response = await self._call_openai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=self.review_model,
                max_tokens=1000,
                temperature=0.5,
            )
        except RuntimeError as e:
            logger.error(f"AI code review failed: {e}")
            return CodeReviewResult(
                overall_feedback="I'm having trouble connecting to the review system right now.",
                strengths=["Your submission has been received."],
                improvements=["Please try again later for a detailed review."],
                rubric_assessment={},
                encouragement="Thanks for your submission!",
            )

        # Parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                review_data = json.loads(json_match.group())
            else:
                review_data = json.loads(response)

            return CodeReviewResult(
                overall_feedback=review_data.get(
                    "overall_feedback", "Review completed."
                ),
                strengths=review_data.get("strengths", []),
                improvements=review_data.get("improvements", []),
                rubric_assessment=review_data.get("rubric_assessment", {}),
                encouragement=review_data.get(
                    "encouragement", "Keep up the good work!"
                ),
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI review response: {e}")
            # Return raw response as feedback
            return CodeReviewResult(
                overall_feedback=response[:500],
                strengths=[],
                improvements=["Please review the feedback above."],
                rubric_assessment={},
                encouragement="Thanks for your submission!",
            )


# Service singleton
_ai_hint_service: Optional[AIHintService] = None


def get_ai_hint_service() -> AIHintService:
    """Get or create AI hint service singleton."""
    global _ai_hint_service
    if _ai_hint_service is None:
        _ai_hint_service = AIHintService()
    return _ai_hint_service
