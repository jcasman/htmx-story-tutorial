import asyncio
import json
from fastapi import FastAPI, Request
import httpx

from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("4-llm-stream.html", {"request": request})


@app.get("/ai")
async def ai():
    async def event_stream():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "http://localhost:11434/api/generate",
            json={
                    "model": "llama3.2",
                    "prompt": "What is the capital of France?",
                }
            ) as resp:
                yield {"event": "status", "data": "Starting event stream<br>"}
                await asyncio.sleep(1)
                print(f"Status Code: {resp.status_code}")
                await asyncio.sleep(1)

                yield {"event": "status", "data": f"Status Code: {resp.status_code}<br>"}
                await asyncio.sleep(1)
                async for line in resp.aiter_lines():
                    # print(line)
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        await asyncio.sleep(0.3)
                        print(f"chunk: {repr(chunk)}")
                        yield {"event": "message", "data": chunk}
                        if data.get("done"):
                            break

                    except json.JSONDecodeError:
                        print(f"Could not decode line: {line}")

                    yield {"event": "message", "data": line + "<br>"}
        await asyncio.sleep(1)
        yield {"event": "close", "data": "Closing event stream"}
    return EventSourceResponse(event_stream())
