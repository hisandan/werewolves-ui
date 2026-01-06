# Copyright 2024 Google LLC
# Modifications for AgentBeats integration
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM API wrapper with support for multiple providers including OpenRouter.

Supported providers:
- OpenAI (direct)
- OpenRouter (any model via OpenAI-compatible API)
- Google Vertex AI / Gemini
- Anthropic (via Vertex AI)

Configuration via environment variables:
- OPENAI_API_KEY: API key for OpenAI or OpenRouter
- OPENAI_API_BASE: Base URL (e.g., https://openrouter.ai/api/v1)
- LLM_MODEL: Model name (e.g., openai/gpt-4o-mini for OpenRouter)
"""

import logging
import os
from typing import Any, Dict, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

# Cached client instance
_openai_client: Optional[OpenAI] = None


def get_openai_client() -> OpenAI:
    """Get or create OpenAI-compatible client (supports OpenRouter)."""
    global _openai_client
    
    if _openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_API_BASE")
        
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable required. "
                "For OpenRouter, use your OpenRouter API key."
            )
        
        if base_url:
            logger.info(f"Using custom API base: {base_url}")
            _openai_client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            _openai_client = OpenAI(api_key=api_key)
    
    return _openai_client


def reset_client():
    """Reset the cached client (useful for testing)."""
    global _openai_client
    _openai_client = None


def generate(
    model: str,
    prompt: str,
    response_schema: Optional[Dict[str, Any]] = None,
    temperature: float = 0.7,
    json_mode: bool = True,
    max_tokens: int = 1024,
    **kwargs,
) -> str:
    """
    Generate text using an LLM.
    
    Automatically routes to the appropriate provider based on:
    1. If OPENAI_API_BASE is set -> Use OpenAI-compatible API (OpenRouter, etc.)
    2. If model contains "gpt" or "/" -> Use OpenAI/OpenRouter
    3. If model contains "claude" -> Use Anthropic via Vertex
    4. Otherwise -> Use Vertex AI (Gemini)
    
    Args:
        model: Model name (e.g., "gpt-4o-mini", "openai/gpt-4o-mini")
        prompt: The prompt to send to the model
        response_schema: Optional JSON schema for structured output
        temperature: Sampling temperature (0.0 - 1.0)
        json_mode: Whether to request JSON output
        max_tokens: Maximum tokens in response
        
    Returns:
        Generated text response
    """
    base_url = os.environ.get("OPENAI_API_BASE")
    
    # Route based on configuration
    if base_url or "gpt" in model.lower() or "/" in model:
        return generate_openai_compatible(
            model=model,
            prompt=prompt,
            json_mode=json_mode,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif "claude" in model.lower():
        return generate_anthropic(model=model, prompt=prompt, max_tokens=max_tokens)
    else:
        return generate_vertexai(
            model=model,
            prompt=prompt,
            temperature=temperature,
            json_mode=json_mode,
            json_schema=response_schema,
        )


def generate_openai_compatible(
    model: str,
    prompt: str,
    json_mode: bool = True,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    **kwargs,
) -> str:
    """
    Generate using OpenAI-compatible API (OpenAI, OpenRouter, Azure, etc.).
    """
    client = get_openai_client()
    
    response_format = {"type": "json_object"} if json_mode else {"type": "text"}
    
    # Some models don't support response_format
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format=response_format,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        # Retry without response_format if not supported
        if "response_format" in str(e).lower():
            logger.warning(f"Model {model} doesn't support response_format, retrying without it")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise
    
    return response.choices[0].message.content or ""


def generate_anthropic(
    model: str,
    prompt: str,
    max_tokens: int = 1024,
    **kwargs,
) -> str:
    """Generate using Anthropic via Vertex AI."""
    try:
        import google.auth
        from anthropic import AnthropicVertex
        
        _, project_id = google.auth.default()
        client = AnthropicVertex(region="us-east5", project_id=project_id)
        
        response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        
        return response.content[0].text
    except ImportError:
        raise ImportError(
            "anthropic and google-auth packages required for Anthropic. "
            "Consider using OpenRouter instead: OPENAI_API_BASE=https://openrouter.ai/api/v1"
        )


def generate_vertexai(
    model: str,
    prompt: str,
    temperature: float = 0.7,
    json_mode: bool = True,
    json_schema: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> str:
    """Generate using Google Vertex AI (Gemini)."""
    try:
        import google.auth
        import vertexai
        from vertexai.preview import generative_models
        
        credentials, project_id = google.auth.default()
        
        vertexai.init(
            project=project_id,
            location="us-central1",
            credentials=credentials,
        )
        
        model_endpoint = generative_models.GenerativeModel(model)
        
        # Flash models don't support constrained decoding
        if "flash" in model:
            json_schema = None
        
        response_mimetype = "application/json" if (json_mode or json_schema) else None
        
        config = generative_models.GenerationConfig(
            temperature=temperature,
            response_mime_type=response_mimetype,
            response_schema=json_schema,
        )
        
        # Safety settings to avoid blocking game content
        safety_config = [
            generative_models.SafetySetting(
                category=generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=generative_models.HarmBlockThreshold.BLOCK_NONE,
            ),
            generative_models.SafetySetting(
                category=generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=generative_models.HarmBlockThreshold.BLOCK_NONE,
            ),
            generative_models.SafetySetting(
                category=generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=generative_models.HarmBlockThreshold.BLOCK_NONE,
            ),
            generative_models.SafetySetting(
                category=generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=generative_models.HarmBlockThreshold.BLOCK_NONE,
            ),
        ]
        
        response = model_endpoint.generate_content(
            prompt,
            generation_config=config,
            stream=False,
            safety_settings=safety_config,
        )
        
        return response.text
        
    except ImportError:
        raise ImportError(
            "google-cloud-aiplatform package required for Vertex AI. "
            "Consider using OpenRouter instead: OPENAI_API_BASE=https://openrouter.ai/api/v1"
        )
