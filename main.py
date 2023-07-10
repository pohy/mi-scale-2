# HTTP server that exposes files from './data' directory

# GET /weights
# Returns list of weights in JSON format
# Example:
# [
#   {
#     "weight": 80.0,
#     "unit": "kg",
#     "timestamp": "2020-01-01T00:00:00.000000Z"
#   },
#   {
#     "weight": 78.3,
#     "unit": "kg",
#     "timestamp": "2020-01-04T00:00:00.000000Z"
#   }
# ]

# Uses fastapi

import uvicorn


import json
import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import FileResponse

from weight import start_weight_listener

# Ensure that data dir exists
if not os.path.exists("./data"):
    os.makedirs("./data")

"""Starts HTTP server that exposes files from './data' directory"""
is_production = os.environ.get("ENV", None) == "production"
port = 80 if is_production else 1337
app = FastAPI(port = port)

"""GET /weights
Returns list of weights in JSON format
Example:
[
    {
        "weight": 80.0,
        "unit": "kg",
        "timestamp": "2020-01-01T00:00:00.000000Z"
    },
    {
        
        "weight": 78.3,
        "unit": "kg",
        "timestamp": "2020-01-04T00:00:00.000000Z"
    }
]
"""
@app.get("/weights")
def get_weights():
    weights = []
    for filename in os.listdir("./data"):
        if not filename.endswith(".json"):
            continue
        with open("./data/" + filename) as f:
            data = json.load(f)
            weights.append(data)

    # Sort by timestamp
    weights.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]))
    return weights

@app.get("/"  )
def get_index():
    return FileResponse("./index.html")

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

if __name__ == "__main__":
    start_weight_listener()
    start_api()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(start_weight_listener),
    #         executor.submit(start_api)
    #     ]
    #     for future in concurrent.futures.as_completed(futures):
    #         print(future.result())
