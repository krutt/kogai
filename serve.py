#!/usr/bin/env python3
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from rizzler import Rizzler, RizzleTemplates
from typing import List, Tuple
from uvicorn import run

templates = RizzleTemplates(directory="templates")

@Rizzler.load_config
def rizzler_settings() -> List[Tuple[str, str]]:
  return [("framework", "react")]

@asynccontextmanager
async def lifespan(_: FastAPI):
  await Rizzler.serve()
  yield
  Rizzler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
  run(app=app)