#!/bin/bash 
for (( i=1; i<=5; i++ ))
    do
        app="nodo$i"
        docker run -d --rm  \
        -p $((i + 4999)):5000 \
        --name=${app} \
        -v "$PWD"/app:/home/nodo/app \
        nodo
        echo $((i + 4999))
        echo "Nodo $i realizado..."
    done
    #
