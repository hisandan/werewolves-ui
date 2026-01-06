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
LLM generation wrapper with retry logic and JSON parsing.
Works with OpenRouter, OpenAI, Vertex AI, and Anthropic.
"""

import dataclasses
import logging
import os
from typing import Any, Dict, List, Optional

import jinja2

from werewolf import apis
from werewolf import utils
from werewolf.utils import Deserializable
from werewolf.config import RETRIES

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LmLog(Deserializable):
    """Log of a language model generation."""
    prompt: str
    raw_resp: str
    result: Any

    @classmethod
    def from_json(cls, data: Dict[Any, Any]):
        return cls(**data)


def format_prompt(prompt_template: str, worldstate: Dict[str, Any]) -> str:
    """Render a Jinja2 template with the given world state."""
    return jinja2.Template(prompt_template).render(worldstate)


def get_default_model() -> str:
    """Get the default model from environment or use gpt-4o-mini."""
    return os.environ.get("LLM_MODEL", "gpt-4o-mini")


def generate(
    prompt_template: str,
    response_schema: Dict[str, Any],
    worldstate: Dict[str, Any],
    model: Optional[str] = None,
    temperature: float = 1.0,
    allowed_values: Optional[List[Any]] = None,
    result_key: Optional[str] = None,
    **kwargs,
) -> tuple[Any, LmLog]:
    """
    Generates text from the language model and parses the result.

    Args:
        prompt_template: The Jinja template for the prompt.
        response_schema: The schema for the expected response.
        worldstate: The world state to be rendered into the prompt.
        model: The language model to use. Defaults to LLM_MODEL env var.
        temperature: The sampling temperature for the language model.
        allowed_values: An optional list of allowed values for the result.
        result_key: An optional key to extract a specific value from the result.

    Returns:
        A tuple containing the result (or None if unsuccessful) and the LmLog.
    """
    # Use default model if not specified
    if model is None:
        model = get_default_model()
    
    prompt = format_prompt(prompt_template, worldstate)
    raw_responses = []
    current_temp = temperature
    
    for attempt in range(RETRIES):
        raw_resp = None
        try:
            raw_resp = apis.generate(
                model=model,
                prompt=prompt,
                response_schema=response_schema,
                temperature=current_temp,
                json_mode=True,
            )
            
            result = utils.parse_json(raw_resp)
            log = LmLog(prompt=prompt, raw_resp=raw_resp, result=result)

            if result and result_key:
                result = result.get(result_key)

            if allowed_values is None or result in allowed_values:
                return result, log

            logger.warning(
                f"Result '{result}' not in allowed values, "
                f"attempt {attempt + 1}/{RETRIES}"
            )

        except Exception as e:
            logger.warning(f"Retrying due to Exception (attempt {attempt + 1}): {e}")
        
        # Increase temperature for retry
        current_temp = min(1.0, current_temp + 0.2)
        if raw_resp:
            raw_responses.append(raw_resp)

    return None, LmLog(
        prompt=prompt,
        raw_resp="-------".join(filter(None, raw_responses)),
        result=None,
    )
