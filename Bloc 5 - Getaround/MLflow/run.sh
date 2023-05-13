docker run -it \
-v "$(pwd):/home/app" \
-p 2000:7000 \
-e PORT=7000 \
mlflow-img