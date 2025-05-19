FROM ubuntu:22.04

EXPOSE 5508

WORKDIR /app

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && \ 
    apt install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install debugpy
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p cache/chat

CMD ["python3"] 
