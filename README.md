### Overview of My Submission
Leveraging **Azure AI form recognizer cognitive** service to automate customer **KYC** verification and validation process. Using this project submission, manual reviewers do not need to analyse and go through each and every submitted document by the customers. The AI service will reject invalid and bogus **KYC** documents.

### Backend API
```
# API to submit KYC document for analysis. 
curl --location --request POST 'https://pan-kyc-automate-1234009.azurewebsites.net/api/kyc-doc-upload' \
--form 'file=@"jS7VOIp6r/image.png"'
```
```
# After submitting document in step 1, you will get requestId in response, You have to use that with other informations that you want to validate.
curl --location --request POST 'https://pan-kyc-automate-1234009.azurewebsites.net/api/kyc-doc-verify' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "D MANIKANDAN",
    "fatherName": "DURAISAMY",
    "pan": "BNZPM2501F",
    "dob": "16/07/1986",
    "requestId": "3c89950b-d282-46c1-9c54-fb565fc1ab20"
}'
```
> Since I am using Azure trial account, so above backend apis will stop working very soon


### Frontend 
👉 go to this static page: ```./frontend/index.html```

### Cloud diagram
![alt text](https://github.com/shivamarora1/kyc-automation-azure-trial-hackathon/blob/main/frontend/Screenshot%202022-03-09%20at%203.23.32%20AM.png)

### Reference:
- https://eastus.dev.cognitive.microsoft.com/docs/services/form-recognizer-api-v3-0-preview-1
- https://docs.microsoft.com/en-us/azure/azure-functions/
- https://azure.microsoft.com/en-in/services/storage/blobs/#overview
- https://azure.microsoft.com/en-in/services/form-recognizer/
