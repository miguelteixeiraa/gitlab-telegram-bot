#!/usr/bin/env python3
from typing import Dict
import json
from flask import Flask, request
import requests

import variables

app = Flask(__name__)

@app.route("/", methods=["POST"])
def merge_requests() -> str:
    message: Dict = {}
    try:
        data: Dict = json.loads(request.data)
        message = {
            "chat_id": variables.CHAT_ID,
            "text": f"""
            *** Evento de merge request na área! Ação: {data['object_attributes']['action'].upper()}***
            De: {data['user']['name']},
            Nome do projeto: {data['object_attributes']['source']['name']},
            Nome da branch: {data['object_attributes']['source_branch']},
            Branch alvo: {data['object_attributes']['target_branch']},
            Titulo do merge request: {data['object_attributes']['title']},
            Descrição: {data['object_attributes']['description']},
            Link: {data['object_attributes']['url']}
         """,
        }
    except Exception as e:
        message = {
            "chat_id": variables.CHAT_ID,
            "text": f"""
            Parece que houve uma movimentação de merge request no gitlab,
            porém um erro ocorreu no processo para trazer os dados para cá :(
            erro:
            {e}
         """,
        }

    #

    chat_endpoint: str = f"{variables.API_PREFIX}{variables.BOT_TOKEN}/sendMessage"

    try:
        requests.post(chat_endpoint, data=message)
        return "OK"

    except Exception as e:
        print("error trying to send message to target channel endpoint")
        return f"FAIL {e}"

    #


#

if __name__ == "__main__":
    app.run(debug=True)
#
