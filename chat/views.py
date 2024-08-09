import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
import google.generativeai as genai

import os

from ai_support import settings
from chat.models import ChatMessage


with open(settings.BASE_DIR / "system_prompt.txt") as f:
    system_prompt = f.read()

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt)

messages = ChatMessage.objects.all()
if len(messages) > 0:
    history = []
    for msg in messages:
        history.append(
            {
                "role": "model" if msg.sender == "SYS" else "user",
                "parts": [
                    {
                        "text": msg.content,
                    }
                ],
            }
        )
    chat = model.start_chat(history=history)
else:
    chat = model.start_chat(history=[])


# Create your views here.
class IndexPage(View):
    def get(self, request):
        chat_history = ChatMessage.objects.all()

        return render(request, "index.html", {"messages": chat_history})


class Reset(View):
    def get(self, request):
        chat.history = []
        ChatMessage.objects.all().delete()
        return redirect(reverse("index"))


class Send(View):
    def post(self, request):
        data = json.loads(request.body)
        response = chat.send_message(data.get("user_input"))

        # Save to db
        usr_message = ChatMessage(
            sender="USR", content=data.get("user_input").replace("\n", "<br>")
        )
        sys_message = ChatMessage(
            sender="SYS", content=response.text.replace("\n", "<br>")
        )
        usr_message.save()
        sys_message.save()

        return JsonResponse(sys_message.serialize(), status=200)
