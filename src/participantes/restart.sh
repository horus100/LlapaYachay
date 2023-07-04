#!/bin/bash 
for (( i=1; i<=5; i++ ))
    do
        app="nodo$i"
        docker restart ${app}
        echo "Nodo $i reiniciado..."
    done

