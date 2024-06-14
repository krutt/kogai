#!/usr/bin/env python3
from asyncio import sleep
from binascii import unhexlify
from bitcointx import select_chain_params
from bitcointx.core.script import (
  CScript,
  OP_ADD,
  OP_1,
  OP_2,
  OP_4,
  OP_5,
  OP_EQUAL,
  TaprootScriptTree,
)
from bitcointx.rpc import RPCCaller
from bitcointx.wallet import P2TRCoinAddress
from bitcointx.wallet import CCoinKey
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from json import dumps
from pydantic import BaseModel, StrictStr
from sse_starlette.sse import EventSourceResponse
from rizzler import Rizzler, RizzleTemplates
from typing import AsyncGenerator, Dict, Literal, Union
from uuid import uuid4 as uuid

select_chain_params("bitcoin/regtest")
templates = RizzleTemplates(directory="templates")


@asynccontextmanager
async def lifespan(_: FastAPI):
  await Rizzler.serve()
  yield
  Rizzler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request})


class LockPayload(BaseModel):
  pubkey: StrictStr


@app.post("/lock")
async def lock(payload: LockPayload) -> Dict[Literal["address"], str]:
  # define the 3 spending equations
  script_a: bytes = CScript([OP_1, OP_ADD, OP_2, OP_EQUAL], name="a")
  script_b: bytes = CScript([OP_2, OP_ADD, OP_4, OP_EQUAL], name="b")
  script_c: bytes = CScript([OP_1, OP_ADD, OP_5, OP_EQUAL], name="c")
  # bitcointx will build a tree of branches and leaves for you
  tree: TaprootScriptTree = TaprootScriptTree([script_a, script_b, script_c])
  # create a provably unspendable public key in order to
  # make the coins spendable ONLY using the script path
  internal_pubkey = CCoinKey.from_secret_bytes(unhexlify(payload.pubkey[2:])).xonly_pub
  tree.set_internal_pubkey(internal_pubkey)
  address: P2TRCoinAddress = P2TRCoinAddress.from_script_tree(tree)
  return {"address": str(address)}


async def blocks_generator() -> (
  AsyncGenerator[Dict[Literal["event", "id", "data"], Union[int, str]], None]
):
  caller: RPCCaller = RPCCaller("http://aesir:aesir@localhost", 18443)
  caller.connect()
  yield {
    "event": "message",
    "id": str(uuid()).replace("-", ""),
    "data": dumps({"blockHash": caller.getbestblockhash()}),
  }
  await sleep(10)


@app.get("/blocks")
def fetch_blocks() -> EventSourceResponse:
  return EventSourceResponse(blocks_generator())


if __name__ == "__main__":
  from uvicorn import run

  run(app=app)

__all__ = ("app",)
