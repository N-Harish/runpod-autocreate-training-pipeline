# Autocreate runpod training flow

* To create a new template and serverless endpoint in runpod run the python program training_pipeline_runpod.py
* The folowing arguments are gien to the program :
  * -t  / --tag: tag of the docker image to create template (for eg :- dev_ml2)
  * -s / --name: Name of the serverless template (for eg :- serverless-dev-ml-2)
  * -e / --endpoint: Name of the serverless endpoint (for eg:- trainer-dev-ml-2)
  * -g / --gpu: GPU types from the following [24_GB_GPU_PRO, 16_GB_GPU, 24_GB_GPU, 48_GB_GPU, 80_GB_GPU]. Defaults to 24_GB_GPU_PRO
  * -w / --worker: No of workers for the endpoint. Defaults to 3
* For example the program cannbe run as follows :-
  ```
  python training_pipeline_runpod.py -t dev_ml4 -s serverless-dev-ml-4-auto -e trainer-dev-ml-4-auto -g 48_GB_GPU
  ```
