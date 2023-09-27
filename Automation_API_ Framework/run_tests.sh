#!/bin/bash

#changing env variable to pytest tags syntax
# wait for availability of source


source_url="http://service.com"
max_retry_count=20
retry_interval=5

# Function to check the status code of the source
check_status_code() {
    local status_code=$(wget --spider --server-response $source_url 2>&1 | grep -E -o 'HTTP/1\.1 [0-9]+ ' | awk '{print $2}')
    echo $status_code
}

retry_count=0
while true; do
    status_code=$(check_status_code)
    if [ $status_code -eq 200 ]; then
        echo "Source is available with status code $status_code"
        break
    else
        echo "Source is not yet available with status code $status_code"
        retry_count=$((retry_count+1))
        if [ $retry_count -eq $max_retry_count ]; then
            echo "Maximum retry count reached. Exiting..."
            exit 1
        fi
        sleep $retry_interval
    fi
done


# run tests
pytest --env="${ENV}" -n 2 --dist=loadscope --reruns 2 --alluredir=reports/allure --junitxml=reports/junit/rep.xml

pwd
cd reports
ls -a

cp -v -R * /reports/
chmod -R a+rw /reports/
