import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest, ratingcosmosbinding: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    request_body = req.get_body()
    productId = req.params.get('productId')
    if not productId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            productId = req_body.get('productId')
    # checking if product exists in the product API
    if productId:
        productIdValue = req.get_json()["productId"]
        prChecker = requests.get(f"https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={productIdValue}")
        productExistCode = prChecker.status_code 
        print (f"{productExistCode} response from product API")
        if (productExistCode==200):
            print(f"{prChecker.json()['productId']},{prChecker.json()['productName']}")
            return func.HttpResponse(f"Success: {prChecker.json()['productName']} with Product Id: {prChecker.json()['productId']} exists in the system",status_code=200)
            ratingcosmosbinding.set(func.Document.from_json(request_body))
        # if product is not in the system
        else:
            return func.HttpResponse(
                "product Id does not exist in the system",
                status_code=400
            )
        
    else:
        return func.HttpResponse(
                "provide productId",
                status_code=400
        )


# def productChecker (productId):



