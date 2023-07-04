#!/bin/bash

        app="cliente"
        docker run -d --rm \
        -p $((5005)):5000 \
        --name=${app} \
        -v "$PWD"/app:/home/nodo/app \
        cliente
        echo $((5005))
        echo "cliente realizado..."

        