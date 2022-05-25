import logging
import azure.functions as func
import json


def main(req: func.HttpRequest, getratings: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')

    if userId:
        if not getratings:
            # no result in query
            logging.info("no result found")
            statusDecription ="Rating Not Found"
            statusCode = 400
            logging.info(statusDecription)
            ratingCheckerResponse = {"ratingStatus":statusCode, "ratingStatusDecription": statusDecription}
            logging.info(ratingCheckerResponse)
            return func.HttpResponse(
                json.dumps(ratingCheckerResponse),
                status_code=statusCode,
                mimetype="application/json"
            )
        else:
            # success scenario
            # logging.info(json.dumps(getratings))
            array =[]
            for doc in getratings:
                tempDic = {
                    "id": doc["id"],
                    "userId": doc["userId"],
                    "productId": doc["productId"],
                    "timestamp": doc["timestamp"],
                    "locationName": doc["locationName"],
                    "rating": doc["rating"],
                    "userNotes": doc["userNotes"]
                }
                array.append(tempDic)
                #  data = doc.to_json()
                # logging.info (f"Document: {doc.to_json()}")
            return func.HttpResponse(
                json.dumps(array),
                status_code=200,
                mimetype="application/json"
            )

    else:
        logging.info("error")
        statusDecription ="User id missing"
        statusCode = 400
        logging.info(statusDecription)
        ratingCheckerResponse = {"ratingStatus":statusCode, "ratingStatusDecription": statusDecription}
        logging.info(ratingCheckerResponse)
        return func.HttpResponse(
            json.dumps(ratingCheckerResponse),
            status_code=statusCode,
            mimetype="application/json"
        )
