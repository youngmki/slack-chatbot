import os
from pprint import pformat
import yaml
from slack import RTMClient
from src.chatbot import ChatBot
from utils.logger import logger


@RTMClient.run_on(event="message")
def dont_say_any_cfdl_bot(**payload) -> None:
    web_client = payload["web_client"]
    data = payload["data"]

    bot_id = data.get("bot_id", "")
    subtype = data.get("subtype", "")
    tag_code = data.get("text", "").split(" ")[0]

    logger.info("The message received is as follows.")
    logger.info(pformat(data))

    if bot_id == "" and subtype == "" and ">" in tag_code:
        channel_id = data["channel"]
        text = data.get("text", "").split(">")[-1].strip()
        message_ts = data["ts"]

        response = chatbot.create(text)
        web_client.chat_postMessage(
            channel=channel_id, text=response, thread_ts=message_ts
        )


if __name__ == "__main__":
    config_path = os.path.join("config/config.yaml")

    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    api_secret_key = config["credentials"]["openai_api_secret_key"]
    bot_user_oauth_token = config["credentials"]["slack_bot_user_oauth_token"]

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

    try:
        rtm_client = RTMClient(token=bot_user_oauth_token)
        logger.info("Your bot is connected and running!")
        rtm_client.start()

    except Exception as error:
        logger.error("An error occurred and the message was: %s", error)
