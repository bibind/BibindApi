from fastapi import FastAPI
from routes import organisation
from kafka.consumer import start_kafka_listener

app = FastAPI(title="SO - Organisation")

# Inclusion des routes
app.include_router(organisation.router)

# Kafka listener
@app.on_event("startup")
async def startup_event():
    start_kafka_listener()
