docker run -it \
-v "$(pwd):/home/app" \
-p 9000:4000 \
-e PORT=4000 \
prediction-chatgpt-img