import requests,json,logging,os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger (kyc-doc-verify) function processed a request.')

    # CREDENTIALS
    FORM_RECOGINZER_KEY = os.getenv("FormRecognizerKey")
    TRAINED_MODEL_ID =os.getenv("TrainedModelId")
    # # # # # #

    try:

        # 1. get all incoming params
        req_body = req.get_json()
        name = req_body.get('name')
        father_name = req_body.get('fatherName')
        pan = req_body.get('pan')
        dob = req_body.get('dob')
        request_id = req_body.get('requestId')

        logging.info("name: {0}, father_name: {1}, pan: {2}, dob: {3}, requestId: {4}".format(
            name, father_name, pan, dob, request_id))

        # 2. call to recognizer to get the analysed params.
        analyzeUrl = "https://eastus.api.cognitive.microsoft.com/formrecognizer/documentModels/" + \
            TRAINED_MODEL_ID+"/analyzeResults/" + \
            request_id+"?api-version=2021-09-30-preview"

        headers = {"Content-Type": "application/json",
                   "Ocp-Apim-Subscription-Key": FORM_RECOGINZER_KEY}
        response = requests.get(analyzeUrl, headers=headers)

        logging.info("response received {0}".format(response.text))
        logging.info("headers received {0}".format(response.headers))
        if response.status_code != 200:
            return func.HttpResponse(status_code=response.status_code)

        resp = response.json()
        documents = resp["analyzeResult"]["documents"][0]["fields"]

        aName = documents["Name"]["content"]
        aPan = documents["PAN number"]["content"]
        aDOB = documents["Date of birth"]["content"]
        aFName = documents["Father Name"]["content"]

        # 3. now compare incoming result.
        success = True
        if aName != name or aPan != pan or aDOB != dob or aFName != father_name:
            success = False

        return func.HttpResponse(json.dumps({"success": success}), status_code=200)
    except Exception as e:
        logging.error(e.args)
        return func.HttpResponse("some error occured", status_code=500)
