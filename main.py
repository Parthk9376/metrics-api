
import os
import time
import uuid
from statistics import mean

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

EMAIL = os.getenv(
    "EXAM_EMAIL",
    "24f2001122@ds.study.iitm.ac.in"
)

ALLOWED_ORIGIN = "https://dash-76j6p5.example.com"


class RequiredHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{elapsed:.6f}"

        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(RequiredHeadersMiddleware)


@app.get("/stats")
def get_stats(values: str = Query(...)):
    try:
        numbers = [int(value.strip()) for value in values.split(",")]

        if not numbers:
            raise ValueError

    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid comma-separated integers"},
        )

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": mean(numbers),
    }
