from fastapi import FastAPI
from routes import release
from kafka.consumer import start_kafka_listener

app = FastAPI(title="SO - Release")

# Inclusion des routes
app.include_router(release.router)

# Kafka listener
@app.on_event("startup")
async def startup_event():
    start_kafka_listener()
