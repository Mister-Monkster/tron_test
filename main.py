import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .dependencies import SessionDep, ClientDep
from .queries import save_request, get_history_query
from .scemas import InfoSchema, HistorySchema

app = FastAPI()


class AddressRequest(BaseModel):
    address: str


@app.post('/get-info')
async def get_info(request: AddressRequest, session: SessionDep, client: ClientDep) -> InfoSchema:
    try:
        balance = await client.get_account_balance(addr=request.address)
        bandwidth = await client.get_bandwidth(addr=request.address)
        energy = await client.get_account_resource(addr=request.address)
        await save_request(request.address, session)
        return InfoSchema(
            address=request.address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy.get("EnergyLimit", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get('/get-history')
async def get_history(session: SessionDep, records: int = 10) -> list[HistorySchema]:
    result = await get_history_query(records, session)
    res = [HistorySchema.model_validate(item) for item in result]
    return res


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000)
