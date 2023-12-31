import json
import os
import pickle

import pandas as pd
from fastapi import FastAPI, Request

from rossmann.Rossmann import Rossmann

# loading model
model = pickle.load(open("./models/xgb_rossmann.pkl", "rb"))

# Initialize FastAPI
app = FastAPI()


@app.post("/rossmann/predict")
async def rossmann_predict(request: Request):
    request_body = await request.body()
    test_json = json.loads(request_body)

    if test_json:
        test_raw = pd.read_json(test_json)

        # Instantiate Rossmann class
        pipeline = Rossmann()

        # Data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        # feature engineering
        df2 = pipeline.feature_eng(df1)
        # data preparation
        df3 = pipeline.data_preparation(df2)
        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response


if __name__ == "__main__":
    import uvicorn

    port = os.environ.get("PORT", 8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
