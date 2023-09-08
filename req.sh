

curl --request POST \
  --header 'content-type: application/json' \
  --url 'https://api.runpod.io/graphql?api_key=R69DUTNS3IDONJ58I2EWXE5N0X0TIG3EFPIIMNNY' \
  --data '{"query": "query myself { myself { containerRegistryCreds{ id name registryAuth } } }" }'