#!/bin/bash

. .venv/bin/activate

dump()
{
#    python manage.py dumpdata auth > ./mainapp/fixtures/dump_auth.json
    python manage.py dumpdata mainapp.ProductCategory > ./mainapp/fixtures/dump_category.json
    python manage.py dumpdata mainapp.Product > ./mainapp/fixtures/dump_product.json
}

load()
{
#    python manage.py loaddata ./mainapp/fixtures/dump_auth.json
    python manage.py loaddata ./mainapp/fixtures/dump_category.json
    python manage.py loaddata ./mainapp/fixtures/dump_product.json
}

usage()
{
    echo "usage $0 [ dump | load ]"
}

parse_args()
{
    if [[ $1 == "dump" ]];
    then
        echo "dump"
        dump
    elif [[ $1 == "load" ]]
    then
        echo "load"
        load
    else
        echo "uknown command $1"
        usage
    fi
}


if [ $# -eq 1 ]
then 
    echo "ok"
    parse_args $1
else
    echo "wrong args count: $#, expect 1"
    usage
fi
