from fastapi import FastAPI
from routes import qualite
from kafka.consumer import start_kafka_listener

app = FastAPI(title="SO - Qualite")

# Inclusion des routes
app.include_router(qualite.router)

# Kafka listener
@app.on_event("startup")
async def startup_event():
    start_kafka_listener()
