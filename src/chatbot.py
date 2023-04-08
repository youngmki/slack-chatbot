import os
from typing import Optional
import yaml
import openai
from utils.logger import logger


class ChatBot:
    def __init__(
        self,
        api_secret_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: int,
        frequency_penalty: int,
        presence_penalty: int,
    ):
        openai.api_key = api_secret_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def create(
        self,
        user_content: str,
        system_content: Optional[str] = None,
        assistant_content: Optional[str] = None,
    ) -> str:
        if self.model == "text-davinci-003":
            completion = openai.Completion.create(
                model=self.model,
                prompt=user_content,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
            return completion["choices"][0]["text"]

        if self.model in ["gpt-3.5-turbo", "gpt-4"]:
            messages = [{"role": "user", "content": user_content}]
            if system_content is not None:
                messages.append({"role": "system", "content": system_content})
            if assistant_content is not None:
                messages.append({"role": "assistant", "content": assistant_content})

            logger.info(messages)
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
            return completion["choices"][0]["message"]["content"]

        msg = f"The model, {self.model} is not supported."
        raise ValueError(msg)

    def answer_directly(self) -> None:
        prompt = input("Enter the prompt: ")
        response = self.create(prompt)
        logger.info(response.strip())


if __name__ == "__main__":
    config_path = os.path.join("config/config.yaml")

    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    api_secret_key = config["credentials"]["openai_api_secret_key"]
    model = config["chatbot"]["model"]
    temperature = config["chatbot"]["temperature"]
    max_tokens = config["chatbot"]["max_tokens"]
    top_p = config["chatbot"]["top_p"]
    frequency_penalty = config["chatbot"]["frequency_penalty"]
    presence_penalty = config["chatbot"]["presence_penalty"]

    chatbot = ChatBot(
        api_secret_key,
        model,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
    )

    while True:
        chatbot.answer_directly()
