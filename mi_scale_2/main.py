import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from mi_scale_2.config import PORT, LOG_LEVEL
from mi_scale_2.weight import start_weight_listener
from mi_scale_2.weight_util import get_saved_weights, keep_only_daily_highest_weight

"""Starts HTTP server that exposes files from './data' directory"""
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
    weights = get_saved_weights()
    weights = keep_only_daily_highest_weight(weights)
    return weights.to_dict("records")

@app.get("/"  )
def get_index():
    return FileResponse("./mi_scale_2/index.html")

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)

if __name__ == "__main__":
    start_weight_listener()
    start_api()
