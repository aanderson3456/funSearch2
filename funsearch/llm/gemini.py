"""Google Gemini LLM implementation supporting Gemini 3.7, 2.5, Flash, Pro."""
from __future__ import annotations

import os
import re
import time
from typing import Any

from absl import logging

from funsearch.llm.base import LLM


def _strip_markdown_code_fences(text: str) -> str:
  """Removes markdown code fences (```python ... ```) if present."""
  text = text.strip()
  # If wrapped entirely in code block
  if text.startswith("```"):
    first_newline = text.find("\n")
    if first_newline != -1:
      text = text[first_newline + 1 :]
    if text.endswith("```"):
      text = text[:-3]
  return text.strip("\n")


class GeminiLLM(LLM):
  """LLM Sampler using the Google GenAI SDK (Gemini 3.7 Flash/Pro, Gemini 2.5)."""

  def __init__(
      self,
      model_name: str = "gemini-3.7-flash",
      api_key: str | None = None,
      samples_per_prompt: int = 1,
      temperature: float = 0.7,
      max_tokens: int = 2048,
      system_instruction: str | None = None,
  ) -> None:
    super().__init__(samples_per_prompt=samples_per_prompt, temperature=temperature)
    self.model_name = model_name
    self.max_tokens = max_tokens
    self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not self.api_key:
      logging.warning(
          "No GEMINI_API_KEY or GOOGLE_API_KEY found in environment or arguments. "
          "Gemini calls will fail unless authenticated via ADC."
      )

    self._client = None
    self._use_legacy = False
    self._system_instruction = system_instruction or (
        "You are an expert mathematician and algorithm designer. "
        "Complete the requested Python function implementation. "
        "Output ONLY the function body code (properly indented with 2 or 4 spaces). "
        "Do NOT include conversational text, explanations, or enclosing markdown tags."
    )

    self._init_client()

  def _init_client(self) -> None:
    try:
      from google import genai
      from google.genai import types
      self._genai = genai
      self._types = types
      if self.api_key:
        self._client = genai.Client(api_key=self.api_key)
      else:
        self._client = genai.Client()
    except Exception as e:
      logging.info(f"Failed to initialize google-genai ({e}), falling back to google.generativeai")
      try:
        import google.generativeai as legacy_genai
        self._legacy_genai = legacy_genai
        if self.api_key:
          self._legacy_genai.configure(api_key=self.api_key)
        self._use_legacy = True
      except Exception as e2:
        raise RuntimeError(f"Could not initialize Google GenAI SDK: {e2}")

  def draw_sample(self, prompt: str) -> str:
    """Generates a single code completion for the prompt."""
    max_retries = 30
    base_delay = 2.0

    for attempt in range(max_retries):
      try:
        if not self._use_legacy and self._client:
          # google-genai v2 client
          config = self._types.GenerateContentConfig(
              temperature=self.temperature,
              max_output_tokens=self.max_tokens,
              system_instruction=self._system_instruction,
          )
          response = self._client.models.generate_content(
              model=self.model_name,
              contents=prompt,
              config=config,
          )
          generated_text = response.text or ""
          return _strip_markdown_code_fences(generated_text)
        else:
          # google.generativeai legacy client
          model = self._legacy_genai.GenerativeModel(
              model_name=self.model_name,
              system_instruction=self._system_instruction,
              generation_config=self._legacy_genai.types.GenerationConfig(
                  temperature=self.temperature,
                  max_output_tokens=self.max_tokens,
              ),
          )
          response = model.generate_content(prompt)
          generated_text = response.text or ""
          return _strip_markdown_code_fences(generated_text)

      except Exception as e:
        err_str = str(e)
        
        # Calculate dynamic delay from API retry recommendations
        delay = base_delay * (2 ** min(attempt, 5))
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
          match = re.search(r'retry in ([0-9.]+)', err_str) or re.search(r"'retryDelay':\s*'([0-9]+)s'", err_str)
          if match:
            delay = float(match.group(1)) + 2.0
          else:
            delay = 35.0
          logging.info(f"Rate quota reached. Pausing {delay:.1f}s before retry ({attempt+1}/{max_retries})...")
        elif "503" in err_str or "UNAVAILABLE" in err_str:
          delay = max(delay, 10.0)
          logging.info(f"Model service spike (503). Pausing {delay:.1f}s before retry ({attempt+1}/{max_retries})...")
        else:
          logging.warning(f"Gemini API generation error (attempt {attempt+1}/{max_retries}): {e}")

        if attempt < max_retries - 1:
          time.sleep(delay)
        else:
          raise e

    return ""
