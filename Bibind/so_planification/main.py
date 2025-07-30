from fastapi import FastAPI
from routes import planification
from kafka.consumer import start_kafka_listener

app = FastAPI(title="SO - Planification")

# Inclusion des routes
app.include_router(planification.router)

# Kafka listener
@app.on_event("startup")
async def startup_event():
    start_kafka_listener()
