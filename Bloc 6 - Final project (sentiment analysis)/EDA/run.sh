docker run -it \
-v "$(pwd):/home/app" \
-p 8000:4000 \
-e PORT=4000 \
chatgpt-eda-img