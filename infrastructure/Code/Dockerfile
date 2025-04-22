# image
FROM python:3.10-slim

# set working directory
WORKDIR /app

# copy files
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy bot source code
COPY . .

# start bot
CMD ["python", "bot.py"]