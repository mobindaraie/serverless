import logging
import requests
import azure.functions as func
import json
import uuid
import datetime
from datetime import timezone
import datetime
  
# Main Function 
def main(req: func.HttpRequest, ratingcosmosbinding: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    request_body = req.get_body()
    
    # Call all product, user and rating validation functions
    productDict = productIdValidation (req)
    userDict = userIdValidation (req)
    ratingDict = validateRating (req)
    
    # Generate output json by merging product, user and rating details, GUID and Time Stamp
    tempResonse = userDict | productDict
    dt = datetime.datetime.now(timezone.utc)
    timestamp = (str(dt).replace('+00:00', 'Z'))
    tempResonse =  {"id":str(uuid.uuid4()),"timestamp":timestamp, "userNotes":req.get_json()["userNotes"], "locationName":req.get_json()["locationName"]} | tempResonse
    tempResonse = tempResonse | ratingDict
    
    # If there is no error (all validations pass), generate json output
    if ((productDict['productStatusCode']==200) and (userDict['userStatusCode']==200 and ratingDict['ratingStatusCode']==200)):
        statusCode=200
        mainKeys = ("id","userId","productId","timestamp","locationName","rating","userNotes")
        responseBody = { your_key: tempResonse[your_key] for your_key in mainKeys }
        # load responseBody to cosmos
        ratingcosmosbinding.set(func.Document.from_json(json.dumps(responseBody)))

        # return response to user
        return func.HttpResponse(
            json.dumps(responseBody),
            status_code=statusCode,
            mimetype="application/json"
        )
        
    else:
        statusCode=400
        errorKeys = ("userStatusCode","userStatusDecription","productStatusCode","productStatusDecription","ratingStatusCode","ratingStatusDecription")
        responseBody = { your_key: tempResonse[your_key] for your_key in errorKeys }
        return func.HttpResponse(
            json.dumps(responseBody),
            status_code=statusCode,
            mimetype="application/json"
        )
        
    return func.HttpResponse(
        json.dumps(tempResonse),
        status_code=statusCode,
        mimetype="application/json"
    )
    

# productIdValidation function validates product a) if it's in request body and b) it's available in the list of products
def productIdValidation (req):
    logging.info("ProductId validation...")
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
        productStatus = productChecker (productIdValue)
        return productStatus
    else:
        statusDecription = "prodcutId is missing from request body"
        statusCode = 400
        logging.info(statusDecription)
        productCheckerResponse = {"productStatusCode":statusCode, "productStatusDecription": statusDecription}
        logging.info(productCheckerResponse)
        return (productCheckerResponse)

# productChecker function checks if the product is available in the list of products
def productChecker (productIdValue):
    logging.info("product being validated agains products API")
    prChecker = requests.get(f"https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={productIdValue}")
    productExistCode = prChecker.status_code
    logging.info (f"{productExistCode} response from product API")
    
    if (productExistCode==200):
        statusDecription = f"Product {prChecker.json()['productName']} exist with productId: {prChecker.json()['productId']}"
        statusCode = 200
        logging.info(statusDecription)
        productCheckerResponse = {"productStatusCode":statusCode, "productStatusDecription": statusDecription} | prChecker.json()
        logging.info(productCheckerResponse)
        return (productCheckerResponse)

    # if product is not in the system
    else:
        statusDecription = "product Id does not exist in the system"
        statusCode = 400
        logging.info(statusDecription)
        productCheckerResponse = {"productStatusCode":statusCode, "productStatusDecription": statusDecription}
        logging.info(productCheckerResponse)
        return (productCheckerResponse)


# userIdValidation function validates product a) if user is in request body and b) it's available in the list of users
def userIdValidation (req):
    logging.info("userId validation...")
    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')
    # checking if product exists in the product API
    if userId:
        userIdValue = req.get_json()["userId"]
        userStatus = userChecker (userIdValue)
        return userStatus
    else:
        statusDecription = "userId is missing from request body"
        statusCode = 400
        logging.info(statusDecription)
        userCheckerResponse = {"userStatusCode":statusCode, "userStatusDecription": statusDecription}
        logging.info(userCheckerResponse)
        return (userCheckerResponse)

# userChecker function checks if the user is available in the list of Users
def userChecker (userIdValue):
    logging.info("user being validated agains users API")
    userChecker = requests.get(f"https://serverlessohapi.azurewebsites.net/api/GetUser?userId={userIdValue}")
    userExistCode = userChecker.status_code 
    logging.info (f"{userExistCode} response from User API")
    
    if (userExistCode==200):

        statusDecription = f"userName {userChecker.json()['userName']} exists with userId: {userChecker.json()['userId']}"
        statusCode = 200
        logging.info(statusDecription)
        userCheckerResponse = {"userStatusCode":statusCode, "userStatusDecription": statusDecription} | userChecker.json()
        logging.info(userCheckerResponse)
        return (userCheckerResponse)  

    # if product is not in the system
    else:
        statusDecription = "User Id does not exist in the system"
        statusCode = 400
        logging.info(statusDecription)
        userCheckerResponse = {"userStatusCode":statusCode, "userStatusDecription": statusDecription}
        logging.info(userCheckerResponse)
        return (userCheckerResponse)

def validateRating (req):
    logging.info("rating validation...")
    rating = req.params.get('rating')
    if not rating:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            rating = req_body.get('rating')
    # checking if product exists in the product API
    if rating:
        if (isinstance(rating, int) and rating<=5 and rating>=0):
            ratingValue = req.get_json()["rating"]
            statusDecription = "Rating Acceptable"
            statusCode = 200
            logging.info(statusDecription)
            ratingCheckerResponse = {"ratingStatusCode":statusCode, "ratingStatusDecription": statusDecription,"rating":ratingValue}
            return (ratingCheckerResponse)       
        else:
            ratingValue = req.get_json()["rating"]
            statusDecription = "Rating Not Acceptable"
            statusCode = 400
            logging.info(statusDecription)
            ratingCheckerResponse = {"ratingStatusCode":statusCode, "ratingStatusDecription": statusDecription,"rating":ratingValue}
            return (ratingCheckerResponse)
    else:
        statusDecription = "Missing Rating"
        statusCode = 400
        logging.info(statusDecription)
        ratingCheckerResponse = {"ratingStatusCode":statusCode, "ratingStatusDecription": statusDecription}
        return (ratingCheckerResponse)  