# image
FROM python:3.13-slim

# set working directory
WORKDIR /app

# copy all files
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# start bot
CMD ["python", "bot.py"]