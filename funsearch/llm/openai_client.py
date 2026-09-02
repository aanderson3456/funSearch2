"""OpenAI-compatible LLM client for FunSearch (OpenAI, Ollama, Groq, vLLM)."""
from __future__ import annotations

import os
import time

from absl import logging

from funsearch.llm.base import LLM


class OpenAILLM(LLM):
  """LLM Sampler for OpenAI-compatible APIs."""

  def __init__(
      self,
      model_name: str = "gpt-4o",
      api_key: str | None = None,
      base_url: str | None = None,
      samples_per_prompt: int = 1,
      temperature: float = 0.7,
      max_tokens: int = 2048,
  ) -> None:
    super().__init__(samples_per_prompt=samples_per_prompt, temperature=temperature)
    self.model_name = model_name
    self.max_tokens = max_tokens
    self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "EMPTY")
    self.base_url = base_url

    import openai
    self._client = openai.OpenAI(
        api_key=self.api_key,
        base_url=self.base_url,
    )

  def draw_sample(self, prompt: str) -> str:
    """Generates code completion via OpenAI-compatible endpoint."""
    max_retries = 3
    base_delay = 2.0

    for attempt in range(max_retries):
      try:
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert mathematician and algorithm designer. "
                        "Complete the requested Python function body. "
                        "Output ONLY the function body code (properly indented). "
                        "Do not include explanation or markdown fences."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        text = response.choices[0].message.content or ""
        text = text.strip()
        if text.startswith("```"):
          lines = text.splitlines()
          text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        return text

      except Exception as e:
        logging.warning(f"OpenAI API call failed (attempt {attempt+1}/{max_retries}): {e}")
        if attempt < max_retries - 1:
          time.sleep(base_delay * (2**attempt))
        else:
          raise e

    return ""
