FROM golang:alpine AS go-builder
WORKDIR /progress
WORKDIR /usr/local/go/src/
COPY scripts/* ./
RUN go build runner.go \
    && chmod +x runner \
    && mv ./runner /progress/runner

FROM alpine AS sql-builder
RUN apk add sqlite
WORKDIR /progress
COPY server/create.sql ./create.sql
RUN sqlite3 datenbank_empty.db < create.sql

FROM python:3.8-alpine AS py-builder
RUN apk add binutils
WORKDIR /progress
COPY server/*.py ./
RUN pip install pip install Flask flask_cors gunicorn eventlet==0.30.2 pyinstaller
RUN pyinstaller \ 
    -F server.py --name server \
    --hidden-import=gunicorn.glogging \
    --hidden-import=gunicorn.workers.sync
RUN cp dist/server ./server && chmod +x server

FROM alpine
WORKDIR /app
COPY --from=go-builder /progress/runner ./runner 
COPY --from=sql-builder /progress/datenbank_empty.db ./datenbank_empty.db
COPY --from=py-builder /progress/server ./server
EXPOSE 8586
CMD ["./runner"]

