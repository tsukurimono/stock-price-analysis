#!/bin/sh
mysqldump -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} candlesticks delistings stocks_tags tags --no-tablespaces > ${1}

