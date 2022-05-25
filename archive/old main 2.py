import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest, ratingcosmosbinding: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    request_body = req.get_body()
    productId = req.params.get('productId')
    # if not productId:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         productId = req.get_json()["productId"]

    if productId:
        productIdValue = req.get_json()["productId"]
        print(productIdValue)
        prChecker = requests.get(f"https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={productIdValue}")
        productExistCode = prChecker.status_code
        print (productExistCode)
        return func.HttpResponse(f"A product with the ID of {productIdValue} Exist in the system",status_code=200)
        ratingcosmosbinding.set(func.Document.from_json(request_body))
        
    else:
        return func.HttpResponse(
                "product does not exist in the system",
                status_code=400
        )



 
    
    
    
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

