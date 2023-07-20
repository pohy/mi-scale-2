import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from mi_scale_2.config import PORT, LOG_LEVEL
from mi_scale_2.weight import start_weight_listener
from mi_scale_2.weight_util import get_saved_weights

# Ensure that data dir exists
if not os.path.exists("./data"):
    os.makedirs("./data")

"""Starts HTTP server that exposes files from './data' directory"""
is_production = os.environ.get("ENV", None) == "production"
app = FastAPI()

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
def _get_weights():
    return get_saved_weights()

@app.get("/"  )
def get_index():
    return FileResponse("./index.html")

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)

if __name__ == "__main__":
    start_weight_listener()
    start_api()