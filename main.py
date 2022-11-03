from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.models.database import database
from app.routers.background_task import router as background_task_router
from app.routers.controllers import router as controllers_router
from app.routers.controller_data import router as controller_data_router
from app.routers.users import router as users_router
from app.routers.token import router as token_router
from app.async_background_task.foton_task import schedular

app = FastAPI()

app.include_router(router=background_task_router)
app.include_router(router=controllers_router)
app.include_router(router=controller_data_router)
app.include_router(router=users_router)
app.include_router(router=token_router)


@app.on_event('startup')
async def startup():
    await database.connect()
    schedular.foton_task_start()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# TEST

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
