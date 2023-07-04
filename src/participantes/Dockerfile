FROM alpine:3.10

RUN apk add --no-cache freetype-dev \
        lcms2-dev openjpeg-dev harfbuzz-dev \
        fribidi-dev 
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev freetype-dev

RUN apk add --no-cache python3-dev \
	&& pip3 install --upgrade pip
RUN apk add --no-cache fping
RUN apk add --no-cache nano
RUN apk add gcc g++ make libffi-dev openssl-dev

RUN adduser -D nodo
USER nodo
WORKDIR /home/nodo
ENV PATH="/home/nodo/.local/bin:${PATH}"

COPY --chown=nodo:nodo requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

RUN mkdir BD  keys

COPY --chown=nodo:nodo . .

CMD ["python3","app/link.py"]

