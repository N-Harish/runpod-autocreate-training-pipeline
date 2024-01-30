import requests
import json
import argparse


def create_serverless_template(image_tag, 
                    name,
                    url='https://api.runpod.io/graphql?api_key=API-KEY', 
                    headers={'content-type': 'application/json'}):
    
    image_name = f"dockerhub-repo/image_name:{image_tag"

    # graphql query for creating template serverless runpod
    # to get container registry auth id run following query
    # query myself { myself { containerRegistryCreds{ id name registryAuth } } }
    query = f'mutation \
        {{ saveTemplate(input:\
            {{ containerDiskInGb: 200, \
                dockerArgs: "", \
                env: [{{ key: "", value: "" }}], \
                imageName: "{image_name}", \
                containerRegistryAuthId: "clhegszyz0001jt08hkgfw4lh", \
                isServerless: true, \
                name: "{name}", \
                readme: "", \
                volumeInGb: 0 }} )\
                {{ containerDiskInGb dockerArgs env {{key value}} id imageName isServerless name readme }} \
        }}'
    
    data = {"query": query }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = response.json()
    tmpId = response['data']['saveTemplate']['id'] 
    return tmpId


def create_serverless_endpoints(template_id,  
                                name,
                                num_workers = 3, 
                                gpu_name = "24_GB_GPU_PRO",
                                url='https://api.runpod.io/graphql?api_key=API-KEY',
                                headers={'content-type': 'application/json'}):
    
    gpu_ids = {
        "24_GB_GPU_PRO": "ADA_24", # 4090
        "16_GB_GPU": "AMPERE_16", # A4000 / A4500
        "24_GB_GPU": "AMPERE_24", # A5000 / A3090
        "48_GB_GPU": "AMPERE_48", # A6000
        "80_GB_GPU": "AMPERE_80" # A100
    }

    gpu_id = gpu_ids[gpu_name]
    query = f'mutation \
        {{ saveEndpoint(input: \
            {{ gpuIds: "{gpu_id}", \
                idleTimeout: 5,\
                locations: "US",\
                name: "{name}",\
                networkVolumeId: "", \
                scalerType: "REQUEST_COUNT",\
                scalerValue: 1,\
                templateId: "{template_id}", \
                workersMax: {num_workers},\
                workersMin: 0}})\
            {{ gpuIds id idleTimeout locations name scalerType scalerValue templateId workersMax workersMin }}\
        }}'

    data = {"query": query }
    response = requests.post(url, headers=headers, data=json.dumps(data)) 
    return response.json()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-t", "--tag", help="Tag of the docker image to use for template (eg :- dev_ml2)", required=True)
    args.add_argument("-s", "--name", help="Name of the template (eg :- serverless-dev-ml-2)", required=True)
    args.add_argument("-e", "--endpoint", help="Name of the endpoint (eg:- trainer-dev-ml-2)", required=True)
    args.add_argument("-g", "--gpu", help="GPU types from the following [24_GB_GPU_PRO, 16_GB_GPU, 24_GB_GPU, 48_GB_GPU, 80_GB_GPU]", default="24_GB_GPU_PRO")
    args.add_argument("-w", "--worker", help="Number of workers for serverless endpoint. Defaults to 3", type= int, default=3)

    arg = vars(args.parse_args())
    
    image_tag = arg.get('tag')
    template_name = arg.get('name')
    gpu_id = arg.get('gpu')
    worker = arg.get('worker')
    endpoint_name = arg.get('endpoint')

    # temp_id = create_serverless_template("dev_ml4", 'serverless-dev-ml-4-auto')
    # create_serverless_endpoints(template_id=temp_id, name="trainer-dev-ml-4-auto",gpu_name="48_GB_GPU")

    temp_id = create_serverless_template(image_tag, template_name)
    create_serverless_endpoints(template_id=temp_id, name=endpoint_name,gpu_name=gpu_id, num_workers=worker)
    
    
