#!/usr/bin/env python3
from asyncio import sleep
from binascii import unhexlify
from bitcointx import select_chain_params
from bitcointx.core import (
  CMutableTransaction,
  COutPoint,
  CTxIn,
  CTxOut,
  CTxInWitness,
  CTxWitness,
  b2x,
  lx,
)
from bitcointx.core.script import (
  CScript,
  CScriptWitness,
  OP_ADD,
  OP_1,
  OP_2,
  OP_4,
  OP_5,
  OP_EQUAL,
  TaprootScriptTree,
)
from bitcointx.rpc import RPCCaller
from bitcointx.wallet import P2TRBitcoinRegtestAddress, P2TRCoinAddress
from bitcointx.wallet import CCoinKey
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from json import dumps
from pydantic import BaseModel, StrictStr
from sse_starlette.sse import EventSourceResponse
from rizzler import Rizzler, RizzleTemplates
from typing import Annotated, AsyncGenerator, Dict, Literal, Union
from uuid import uuid4 as uuid


select_chain_params("bitcoin/regtest")


@asynccontextmanager
async def lifespan(_: FastAPI):
  await Rizzler.serve()
  caller: RPCCaller = RPCCaller("http://aesir:aesir@localhost", 18443)
  caller.connect()
  if len(caller.listwallets()) == 0:
    caller.createwallet("default", False, False)
    treasury = caller.getnewaddress()
    caller.generatetoaddress(100, treasury)
  yield
  Rizzler.shutdown()


def taproot_script_tree() -> TaprootScriptTree:
  ### define the 3 spending equations ###
  script_a: bytes = CScript([OP_1, OP_ADD, OP_2, OP_EQUAL], name="a")
  script_b: bytes = CScript([OP_2, OP_ADD, OP_4, OP_EQUAL], name="b")
  script_c: bytes = CScript([OP_1, OP_ADD, OP_5, OP_EQUAL], name="c")
  ### bitcointx will build a tree of branches and leaves for you ###
  return TaprootScriptTree([script_a, script_b, script_c])


def rpc_caller() -> RPCCaller:
  caller: RPCCaller = RPCCaller("http://aesir:aesir@localhost", 18443)
  caller.connect()
  return caller


app = FastAPI(lifespan=lifespan)
templates = RizzleTemplates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
  return templates.TemplateResponse("index.html", {"request": request})


async def blocks_generator(
  caller: RPCCaller,
) -> AsyncGenerator[Dict[Literal["event", "id", "data"], Union[int, str]], None]:
  caller.connect()
  yield {
    "event": "message",
    "id": str(uuid()).replace("-", ""),
    "data": dumps({"blockHash": caller.getbestblockhash()}),
  }
  await sleep(10)


@app.get("/balance/{address}")
async def fetch_balance(
  address: str, caller: Annotated[RPCCaller, Depends(rpc_caller)]
) -> Dict[Literal["balance"], float]:
  txouts: dict = caller.scantxoutset("start", [{"desc": f"addr({ address })"}])
  caller.scantxoutset("abort", [{"desc": f"addr({ address })"}])
  return {"balance": txouts.get("total_amount", 0.0)}


@app.get("/blocks")
def fetch_blocks(caller: Annotated[RPCCaller, Depends(rpc_caller)]) -> EventSourceResponse:
  return EventSourceResponse(blocks_generator(caller))


class FaucetPayload(BaseModel):
  address: StrictStr


@app.post("/faucet")
async def faucet(caller: Annotated[RPCCaller, Depends(rpc_caller)], payload: FaucetPayload) -> str:
  caller.generatetoaddress(6, payload.address)
  return "OK"


class LockPayload(BaseModel):
  pubkey: StrictStr


@app.post("/lock")
async def lock(
  payload: LockPayload, tree: Annotated[TaprootScriptTree, Depends(taproot_script_tree)]
) -> Dict[Literal["address"], str]:
  ### create a provably unspendable public key in order to ###
  ### make the coins spendable ONLY using the script path ###
  internal_pubkey = CCoinKey.from_secret_bytes(unhexlify(payload.pubkey[2:])).xonly_pub
  tree.set_internal_pubkey(internal_pubkey)
  address: P2TRCoinAddress = P2TRCoinAddress.from_script_tree(tree)
  return {"address": str(address)}


class SendPayload(BaseModel):
  address: StrictStr
  amount: float


@app.post("/send")
async def send_payment(
  caller: Annotated[RPCCaller, Depends(rpc_caller)], payload: SendPayload
) -> Dict[Literal["txid"], str]:
  txid: str = caller.sendtoaddress(payload.address, payload.amount)
  return {"txid": txid}


class UnlockPayload(BaseModel):
  address: StrictStr
  pubkey: StrictStr
  txid: StrictStr


@app.post("/unlock")
async def send_unlock_payment(
  caller: Annotated[RPCCaller, Depends(rpc_caller)],
  tree: Annotated[TaprootScriptTree, Depends(taproot_script_tree)],
  payload: UnlockPayload,
) -> Dict[Literal["txid"], str]:
  internal_pubkey = CCoinKey.from_secret_bytes(unhexlify(payload.pubkey[2:])).xonly_pub
  tree.set_internal_pubkey(internal_pubkey)
  ### set the new destination address ###
  destination_address = P2TRBitcoinRegtestAddress(payload.address)

  ### construct a spending transaction ###
  script, control_block = tree.get_script_with_control_block("b")  # type: ignore

  ### get the txid and index of the transaction that funded the ###
  ### address which we generated above ###
  txin = CTxIn(COutPoint(lx(payload.txid), 1))
  txout = CTxOut(998000, destination_address.to_scriptPubKey())
  tx = CMutableTransaction([txin], [txout])

  ### we pass the encoded num 2 (x + 2 = 4; x = 4 - 2; x = 2) which is the answer ###
  ### to script b that we are using to unlock the funds ###
  ctxinwitnesses = [CTxInWitness(CScriptWitness([2, script, control_block]))]
  tx.wit = CTxWitness(ctxinwitnesses)  # type: ignore

  ### Broadcast ###
  try:
    return {"txid": caller.sendrawtransaction(b2x(tx.serialize()), 0)}
  except Exception as err:
    print(err)
    return {"txid": ""}


if __name__ == "__main__":
  from uvicorn import run

  run(app=app)

__all__ = ("app",)
