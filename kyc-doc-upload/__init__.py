import logging,requests,json,os

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger (kyc-doc-upload) function processed a request.')

    # CREDENTIALS
    CONTAINER_NAME = os.getenv("ContainerName")
    CONNECTION_STRING = os.getenv("ConnectionString")

    FORM_RECOGINZER_KEY = os.getenv("FormRecognizerKey")
    TRAINED_MODEL_ID =os.getenv("TrainedModelId")
    # # # # # #

    try:

        # 1. upload file to azure storage
        file = req.files.get('file')
        fileName = file.filename
        logging.info("received file to upload: {0}".format(fileName))

        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, blob=fileName)
        blob_client.upload_blob(file, overwrite=True)

        uploadedUrl = "https://kycautomatestorageacc.blob.core.windows.net/" + \
            CONTAINER_NAME+"/"+fileName
        logging.info('file uploaded to: {0}'.format(uploadedUrl))
        ####

        logging.info('going to make recognizer call for {0} url'.format(uploadedUrl))

        # 2. send it for recognizer
        analyzeUrl = "https://eastus.api.cognitive.microsoft.com/formrecognizer/documentModels/" + \
            TRAINED_MODEL_ID+":analyze?api-version=2021-09-30-preview&stringIndexType=textElements"
        postData = {'urlSource': uploadedUrl}
        headers = {"Content-Type": "application/json",
                   "Ocp-Apim-Subscription-Key": FORM_RECOGINZER_KEY}
        response = requests.post(analyzeUrl, json=postData, headers=headers)

        logging.info("response received {0}".format(response.text))
        logging.info("headers received {0}".format(response.headers))

        requestId = response.headers['apim-request-id']
        return func.HttpResponse(json.dumps({"requestId": requestId}), status_code=response.status_code)
    except Exception as e:
        logging.error(e.args)
        return func.HttpResponse("some error occured", status_code=500)
