import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest, ratingcosmosbinding: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    request_body = req.get_body()
    productId = req.get_json()["productId"]
    print(productId)
    page = requests.get(f"https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={productId}")
    productExistCode = page.status_code
    print (productExistCode)
    # if not productExistCode:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    # ratingcosmosbinding.set(func.Document.from_json(request_body))
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    #     ratingcosmosbinding.set(func.Document.from_json(request_body))
        
    # else:
    # productExist = productExistResponse.headers
    return func.HttpResponse(
            "test",
            status_code=200
    )

