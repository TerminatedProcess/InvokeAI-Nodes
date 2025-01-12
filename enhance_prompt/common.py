# Copyright (c) 2024 Lincoln D. Stein

from pydantic import BaseModel, Field, PrivateAttr
from typing import Tuple
from types import ModuleType

class OllamaSettings(BaseModel):
    """Common configuration settings for Ollama"""

    prompt_prefix: str = Field(
        default="", description="Prompt prefix for this model's operation"
    )
    ollama_available: bool = Field(
        default=False, description="Is the Ollama module installed?"
    )
    models: Tuple[str] = Field(
        default_factory=tuple, description="List of Ollama model names"
    )
    message: str = Field(
        default="", description="An error message to display when a prereq is missing"
    )
    ollama: ModuleType = Field(
        default=None,
        description="Ollama module to use"
    )

    class Config:
        arbitrary_types_allowed=True

    def model_post_init(self, __context) -> None:
        """Import ollama and other dependencies."""
        try:
            import ollama

            self.ollama_available = True
            self.ollama = ollama
        except ImportError:
            self.message += "To use this node, please run 'pip install ollama==0.3.3'"

        if not self.ollama_available:
            return

        llms = ollama.list()
        self.models = tuple(sorted(model["name"] for model in llms["models"]))
