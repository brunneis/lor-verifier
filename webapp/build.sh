#!/bin/bash
source env.sh
cp index.html.template index.html
sed -i "s~%API_ENDPOINT%~$API_ENDPOINT~" index.html