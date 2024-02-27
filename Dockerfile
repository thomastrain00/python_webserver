FROM debian:bookworm
RUN apt update && apt install python3 -y
WORKDIR /web_server
ADD src .
CMD ["python3","web_server.py"] 
