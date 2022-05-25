import logging
import json

import azure.functions as func


def main(req: func.HttpRequest, getcosmosrating: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    # try: 
        
    # except ValueError:
    #     statusDecription ="Rating id missing"
    #     statusCode = 400
    #     logging.info(statusDecription)
    #     ratingCheckerResponse = {"ratingStatus":statusCode, "ratingStatusDecription": statusDecription}
    #     logging.info(ratingCheckerResponse)
    #     return func.HttpResponse(
    #         json.dumps(ratingCheckerResponse),
    #         status_code=statusCode,
    #         mimetype="application/json"
    #     )

    ratingId = req.params.get('ratingId')

    if not ratingId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
            
        else:
            ratingId = req_body.get('ratingId')

    if ratingId:
        if not getcosmosrating:
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
            for doc in getcosmosrating:
                data = json.loads(doc.to_json())
                logging.info (f"Document: {doc.to_json()}")
            return func.HttpResponse(
                doc.to_json(),
                status_code=200,
                mimetype="application/json"
            )
        # return func.HttpResponse(f"Hello, {id}. This HTTP triggered function executed successfully.")

    else:
        logging.info("error")
        statusDecription ="Rating id missing"
        statusCode = 400
        logging.info(statusDecription)
        ratingCheckerResponse = {"ratingStatus":statusCode, "ratingStatusDecription": statusDecription}
        logging.info(ratingCheckerResponse)
        return func.HttpResponse(
            json.dumps(ratingCheckerResponse),
            status_code=statusCode,
            mimetype="application/json"
        )
