import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from router.dispatcher import route_request
from assistants import assistant1, assistant2, assistant3

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>AI Conductor Chat</title>
    </head>
    <body>
        <h1>AI Conductor</h1>
        <textarea id="chat" rows="20" cols="100" readonly></textarea><br>
        <input type="text" id="message" size="100" autofocus/>
        <button onclick="sendMessage()">Send</button>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                const chat = document.getElementById("chat");
                chat.value += event.data + "\n";
            };
            function sendMessage() {
                const input = document.getElementById("message");
                ws.send(input.value);
                input.value = "";
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        routed = route_request(data)
        question = routed["question"]
        assistant_id = routed["assistant"]

        if assistant_id == "1":
            answer = assistant1.answer(question)
        elif assistant_id == "2":
            answer = assistant2.answer(question)
        elif assistant_id == "3":
            answer = assistant3.answer(question)
        else:
            answer = "Извините, я не смог определить подходящего ассистента."

        response = f"{routed['assistant_name']}: {answer}"
        await websocket.send_text(response)