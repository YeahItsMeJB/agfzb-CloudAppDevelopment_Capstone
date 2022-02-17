#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests

def main(dict):
    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])
        response = service.post_all_docs(db='reviews',include_docs=True).get_result()
        data = list(map((lambda x: x["doc"]), response["rows"]))
        print(data)
    except ApiException as ae:
        print("unable to connect")
        return {"error": ae}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": data}

