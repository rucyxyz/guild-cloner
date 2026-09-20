from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import json

from cloner import DiscordCloner

app = FastAPI()
cloner = DiscordCloner()

# 進捗を送るWebSocket接続を保持
active_ws: list[WebSocket] = []


class LoginReq(BaseModel):
    token: str


class CloneReq(BaseModel):
    token: str
    src_id: str
    dst_id: str
    options: dict


async def broadcast(message: str, percent: int):
    payload = json.dumps({"message": message, "percent": percent}, ensure_ascii=False)
    for ws in list(active_ws):
        try:
            await ws.send_text(payload)
        except Exception:
            active_ws.remove(ws)


@app.post("/api/login")
async def api_login(req: LoginReq):
    try:
        guilds = await cloner.get_guilds(req.token)
        return {"ok": True, "guilds": guilds}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=400)


@app.post("/api/clone")
async def api_clone(req: CloneReq):
    try:
        src_id = int(req.src_id)
        dst_id = int(req.dst_id)
    except ValueError:
        return JSONResponse({"ok": False, "error": "IDは数値で入力してください"}, status_code=400)

    # バックグラウンドで開始
    asyncio.create_task(
        cloner.clone(req.token, src_id, dst_id, req.options, broadcast)
    )
    return {"ok": True}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    active_ws.append(ws)
    try:
        while True:
            await ws.receive_text()  # keep-alive
    except WebSocketDisconnect:
        active_ws.remove(ws)


app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
