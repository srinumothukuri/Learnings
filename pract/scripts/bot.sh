#!/bin/bash

for i in {1..10}; do
    echo -ne "$i\033[0K\r"
    sleep 1
done

echo "Done!"

