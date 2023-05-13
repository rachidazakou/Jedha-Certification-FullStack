import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from typing import Optional

description = """
Hello, welcome to Getaround's API.

## Introduction Endpoints

You have two endpoints you can try:
* `/`: **GET** request that display a simple default message.
* `/preview`: **GET** request to get a sample of the dataset.
* `/predict`: **POST** request to get predictions.

"""

tags_metadata = [
    {
        "name": "Infos",
        "description": "Redirect to the `/docs` section."
    },
    
    {
        "name": "Preview",
        "description": "Give a sample of the data.",
    },

    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]

app = FastAPI(
    title="🚗 Getaround pricing optimization API",
    description=description,
    version="0.1",
    contact={
        "name": "GetAround"
    },
    openapi_tags=tags_metadata
)


class PredictionFeatures(BaseModel):
    model_key: str="Renault"
    mileage: int=10000
    engine_power: int=100
    fuel: str="petrol"
    paint_color: str="black"
    car_type: str="convertible"
    private_parking_available: bool=True
    has_gps: bool=True
    has_air_conditioning: bool=True
    automatic_car: bool=False
    has_getaround_connect: bool=True
    has_speed_regulator: bool=True
    winter_tires: bool=False


@app.get("/", tags=["Infos"])
async def index():
    """
    Returns a welcome message.
    """
    message = "Hello, if you want to learn more, check out the documentation of the api at `/docs`"
    return message



@app.get("/preview", tags=["Preview"])
async def dataset_sample(rows: Optional[int] = 5):
    """
    Returns a sample of the dataset.
    You can specify the number of rows you want, by indicating a value for `rows`, default is `5`.
    """
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
    sample = df.sample(rows)
    return sample.to_json()


@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction of rental price. 
    """
    
    df = pd.DataFrame(dict(predictionFeatures), index=[0])

    logged_model = 'runs:/a99dfaa0b76e4780a0f6cbdeb0c18aff/model'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True, reload=True)
