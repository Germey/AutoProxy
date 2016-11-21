#!/bin/bash

if [ "$#" != 1 ];then
	echo "param error."
	exit 0
fi

KEY=""
SERVER=""


load_config() {
	cfg=$1;
	content=`cat ${cfg}`;
	KEY=`echo "${content}" |grep 'KEY'| sed 's/^KEY=[\"]\(.*\)[\"]/\1/'`;
	SERVER=`echo "${content}" |grep 'SERVER'| sed 's/^SERVER=[\"]\(.*\)[\"]/\1/'`;
	KEY=${KEY:4}
	SERVER=${SERVER:7}
}

change_proxy() {
    . ./pppoe.sh
}

send_request() {
    echo $SERVER/$KEY;
    curl $SERVER/$KEY;
}

main() {
    load_config $1
    change_proxy
    send_request
}

main $1