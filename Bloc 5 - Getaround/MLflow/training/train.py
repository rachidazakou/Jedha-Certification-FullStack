import mlflow
from mlflow.models.signature import infer_signature
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import time


EXPERIMENT_NAME="getaround-pricing-optimization"

# Instanciate experiment
client = mlflow.tracking.MlflowClient()

mlflow.set_tracking_uri("https://mlflow-web-app.herokuapp.com")


# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get experiment's info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
# run = client.create_run(experiment.experiment_id) 


# Import data
df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
df.drop(df.columns[0], axis=1, inplace=True)
df = df[~df.model_key.isin(['Mini', 'Mazda', 'Honda', 'Yamaha'])] # Drop cars with few occurrences (1 or 2)
df = df[(df.mileage>0) | (df.engine_power>0)] # drop outliers

# Split features in categorical and numeric
features = np.delete(df.columns, -1)
numeric_features = []
categorical_features = []

for col in features:
    if ('float' in str(df[col].dtype).lower()) or ('int' in str(df[col].dtype).lower()):
        numeric_features.append(col)
    else:
        categorical_features.append(col)

# Preprocessor instanciation
categorical_transformer = OneHotEncoder(drop='first', handle_unknown='error')
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_transformer, categorical_features),
        ("num", numeric_transformer, numeric_features)
    ])

X = df.drop('rental_price_per_day', axis=1)
y = df['rental_price_per_day']

# Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)


start_time = time.time()

mlflow.sklearn.autolog()

# ******** random forest ********#
params_rf = {'n_estimators': [10, 20, 30, 40],
            'max_depth': [2, 4, 6, 8, 10],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]}

model = Pipeline(steps=[
    ("Preprocessing", preprocessor),
    ("Regressor", GridSearchCV(RandomForestRegressor(), params_rf, cv=3))
], verbose=True)


with mlflow.start_run():

    model.fit(X_train, y_train)

    print("Linear regression performances : ")
    print("R2 score on training set : ", r2_score(y_train, model.predict(X_train)))
    print("R2 score on test set : ", r2_score(y_test, model.predict(X_test)))

    predictions = model.predict(X_train)

    mlflow.log_metric("training_r2_score", r2_score(y_train, model.predict(X_train)))
    mlflow.log_metric("test_r2_score", r2_score(y_test, model.predict(X_test)))
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
