from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from gradio_client import Client

app = FastAPI()

# Allow requests from specified origins
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoringItem(BaseModel):
    message: str

client = Client("https://givyboy-mental-health-chatbot.hf.space/--replicas/04p3w/", verbose=True)

@app.post("/predict")
async def predict(item: ScoringItem):
    try:
        result = client.predict(item.message, api_name="/chat")
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")