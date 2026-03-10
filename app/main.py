import logging
import random
import string
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.models import ShortenRequest, ShortenResponse
from app.db import init_db, get_connection
from app.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

ALPHABET = string.ascii_letters + string.digits

app = FastAPI(title="URL shorten")


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Application startup")
    init_db()


@app.post("/shorten", response_model=ShortenResponse)
def shorten(request: ShortenRequest):
    """
    Принимает длинную ссылку,
    возвращает короткий URL
    """
    with get_connection() as conn:
        code = "".join(random.choices(ALPHABET, k=6))
        logger.info("Creating short url", extra={"code": code})
        try:
            conn.execute(
                """
                INSERT INTO Shorten(code, original_url) 
                VALUES (?, ?)
                """,
                (code, str(request.url))
            )
            conn.commit()
            logger.info(
                "Short url created",
                extra={"code": code, "url": str(request.url)},
            )
            return {"short_url": f"http://localhost:8000/{code}"}
        except Exception:
            logger.exception("Failed to create short url")
            raise HTTPException(
                status_code=500,
                detail="Не удалось сгенерировать короткий url",
            )


@app.get("/{code}")
def redirect_url(code: str):
    """
    Делает редирект
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT original_url FROM Shorten WHERE code = ?",
            (code,),
        ).fetchone()
        if row is None:
            logger.warning("Short url not found", extra={"code": code})
            raise HTTPException(status_code=404, detail="URl not found")
        conn.execute(
            "UPDATE Shorten SET clicks = clicks + 1 WHERE code = ?",
            (code,),
        )
        conn.commit()
        logger.info(
            "Redirect",
            extra={"code": code, "target": row["original_url"]},
        )

        return RedirectResponse(url=row["original_url"])


@app.get("/stats/{code}")
def get_stats(code: str):
    """
    Возвращает количество переходов
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT clicks FROM Shorten WHERE code = ?",
            (code,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="URL not found")

        return {
            "code": code,
            "clicks": row["clicks"]
        }
