## This directory contains the luigi file to download all the merged data along with the data that contains the calculated heuristics that will be used for restocking purposes in the application

### The below command can be used to run the pipeline

python instacartluigi.py uploadziptos3 --local-scheduler --akey "your access key" --skey "your secret access key"

### For ease of user we have also Dockerized the whole luigi pipeline you can run it using the following commands

####  docker pull tushargl016/luigiinstacartpipeline
####  docker run -e akey=awsaccesskey -e skey=awssecretkey  -ti tushargl016/luigiinstacartpipeline

#### Or if you want you can build your own docker image using the following commands
    To build locally and run
    docker build -f dock -t luigiinstacartpipeline .
    docker run -e akey=awsaccesskey -e skey=awssecretkey -ti luigiinstacartpipeline
    
    #### you can push this image to your dockerhub using 
    
    docker tag <imageid> <username>/luigiinstacartpipeline:latest
    Docker push <username>/luigiinstacartpipeline
    
### Note: Make sure you provide your AWS access key and secret access key or the job will fail because the data will be uploaded to your se bucket
