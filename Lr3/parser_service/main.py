import httpx
from fastapi import FastAPI, HTTPException
from pydantic import AnyHttpUrl, BaseModel

from shared.parser_logic import UnsafeUrlError, parse_and_save


class ParseRequest(BaseModel):
    url: AnyHttpUrl
    user_id: int = 1


app = FastAPI(title="TimeFlow Parser", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
def parse_page(payload: ParseRequest) -> dict[str, object]:
    try:
        return parse_and_save(str(payload.url), payload.user_id)
    except UnsafeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Сайт недоступен: {exc}") from exc
