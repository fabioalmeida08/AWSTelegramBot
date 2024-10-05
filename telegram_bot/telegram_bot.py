import requests
import boto3
import json
from helpers import get_formated_date

data_formatada = get_formated_date()


class TelegramBot:
    def __init__(self, event):
        self.bot_token_parameter = "/Telegram/TokenBot"
        self.chat_id_parameter = "/Telegram/MyChatID"
        self.event_resource = event.get("resource", False)
        self.event_body = self._parse_event_body(event)

        self.success = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "mensagem enviada com sucesso",
                    "date": f"{data_formatada}",
                }
            ),
        }

        self.error = {"statusCode": 500, "body": json.dumps("erro ao enviar mensagem")}
        self.timeout_error = {
            "statusCode": 504,
            "body": json.dumps("Timeout ao enviar mensagem para o Telegram"),
        }

    def _parse_event_body(self, event):
        body = event.get("body", None)
        if body:
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                print("Erro ao decodificar JSON.")
                return False
        return False

    def _send_telegram_message(self, message):
        try:
            ssm = boto3.client("ssm")

            bot_token = ssm.get_parameter(
                Name=self.bot_token_parameter, WithDecryption=True
            )["Parameter"]["Value"]

            chat_id = ssm.get_parameter(
                Name=self.chat_id_parameter, WithDecryption=True
            )["Parameter"]["Value"]

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

            data = {
                "chat_id": chat_id,
                "text": message,
            }

            response = requests.post(url, json=data, timeout=5)

            if response.status_code >= 200:
                return self.success
            else:
                return self.error
        except Exception as e:
            print(f"Erro ao enviar mensagem para o Telegram: {e}")
            return self.error
        except requests.Timeout:
            return self.timeout_error

    def process_event(self):

        if self.event_resource:
            if self.event_resource == "/notify":
                message = self.event_body.get("message")
                print(message)
                if not message:
                    return self.error
                return self._send_telegram_message(message=message)
        return self.error