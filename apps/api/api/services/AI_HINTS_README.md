# AI Hints System

This module provides AI-powered hints, error explanations, and code review capabilities for the Python OOP Journey platform.

## Overview

The AI Hints System uses OpenAI's GPT models to provide contextual assistance to learners:

1. **Hint Generation** - Three levels of guided hints
2. **Error Explanation** - Plain English explanations of Python errors
3. **Code Review** - AI-powered review of project submissions

## Architecture

```
api/
├── prompts/
│   ├── __init__.py          # Prompt exports
│   └── hints.py             # Prompt templates for AI
├── routers/
│   └── ai.py                # FastAPI endpoints
├── schemas/
│   └── ai_hints.py          # Pydantic schemas
└── services/
    └── ai_hints.py          # AI service implementation
```

## Configuration

Add to `.env`:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-...

# Optional: Anthropic API Key
ANTHROPIC_API_KEY=

# Model Configuration
AI_HINT_MODEL=gpt-4o-mini      # For hints and error explanations
AI_REVIEW_MODEL=gpt-4o         # For code reviews
AI_RATE_LIMIT_PER_HOUR=10
AI_CACHE_TTL_HOURS=24
```

## API Endpoints

### Generate Hint
```http
POST /api/v1/ai/hint
Rate Limit: 10/hour

{
  "problem_slug": "w01d01-hello-object",
  "code": "def greet(): pass",
  "hint_level": 1,
  "test_results": {...},
  "previous_hints": []
}

Response:
{
  "hint": "Think about what data structure...",
  "relevant_lines": [5, 12],
  "explanation": "Level 1 hint for w01d01-hello-object",
  "hint_level": 1
}
```

### Explain Error
```http
POST /api/v1/ai/explain-error
Rate Limit: 20/hour

{
  "error_message": "NameError: name 'x' is not defined",
  "code": "print(x)",
  "problem_slug": "w01d01-hello-object"
}

Response:
{
  "explanation": "Python can't find a variable named 'x'...",
  "suggestion": "Define x before using it...",
  "relevant_lines": [1]
}
```

### Code Review
```http
POST /api/v1/ai/code-review
Rate Limit: 5/hour

{
  "files": {"main.py": "...", "utils.py": "..."},
  "project_slug": "w02-bank-account",
  "rubric": [...]
}

Response:
{
  "overall_feedback": "Good structure but needs...",
  "strengths": ["Clean code", "Good naming"],
  "improvements": ["Add docstrings", "Handle edge cases"],
  "rubric_assessment": {...},
  "encouragement": "Keep up the good work!"
}
```

## Hint Levels

### Level 1: Conceptual Nudge
- High-level guidance
- Asks leading questions
- No implementation details

Example: "Think about what data structure might help you organize this information efficiently..."

### Level 2: Structural Guidance
- Code organization advice
- Pattern suggestions
- Structure without syntax

Example: "Consider breaking this into smaller functions..."

### Level 3: Specific Suggestion
- Points to specific lines
- Identifies bugs/edge cases
- Suggests specific features

Example: "On line 15, you might want to check if the list is empty..."

## Safety Features

1. **Content Filtering** - Checks for prompt injection attempts
2. **No Complete Solutions** - Prompts strictly forbid giving away answers
3. **Rate Limiting** - Per-user rate limits prevent abuse
4. **Caching** - Reduces costs by caching common hints
5. **Logging** - All interactions logged for review

## Cost Optimization

- **Model Selection**: Uses cheaper `gpt-4o-mini` for hints, `gpt-4o` only for code reviews
- **Token Limits**: Hints limited to 200 tokens
- **Caching**: In-memory cache (Redis in production)
- **Context Management**: Only last 3 hint exchanges included

## Frontend Components

### React Components

```typescript
// AI Hint Card
<AIHintCard
  hint="..."
  relevantLines={[1, 5]}
  hintLevel={1}
  onFeedback={(helpful) => ...}
  onHighlightLines={(lines) => ...}
/>

// Error Explainer
<ErrorExplainer
  errorMessage="..."
  code="..."
  problemSlug="..."
  onExplain={async () => {...}}
/>

// Code Review Panel
<CodeReviewPanel
  files={{"main.py": "..."}}
  projectSlug="..."
  rubric={[...]}
/>
```

### React Hook

```typescript
const {
  hint,
  isLoadingHint,
  generateHint,
  explainError,
  errorExplanation,
} = useAIHints({
  problemSlug,
  code,
  testResults,
});
```

## Testing

1. Write broken code in the editor
2. Click "Get AI Hint" button
3. Verify hint guides without giving solution
4. Run code with errors
5. Click "Explain this error"
6. Submit project and request code review

## Future Enhancements

- [ ] Conversation history persistence
- [ ] Learner progress-based personalization
- [ ] Multi-language support
- [ ] Advanced rubric checking
- [ ] Peer comparison insights
