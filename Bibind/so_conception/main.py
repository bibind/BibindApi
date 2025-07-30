from fastapi import FastAPI
from routes import conception
from kafka.consumer import start_kafka_listener

app = FastAPI(title="SO - Conception")

# Inclusion des routes
app.include_router(conception.router)

# Kafka listener
@app.on_event("startup")
async def startup_event():
    start_kafka_listener()
