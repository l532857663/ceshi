#! /bin/bash

SYS_DT="$(date +%F-%T)"

echo $SYS_DT

cat > ceshi <<EOF
hahahah	$SYS_DT
EOF
