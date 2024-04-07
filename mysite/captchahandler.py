# api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import requests

YOUR_SECRET_KEY_V2 = "6LchCrMpAAAAAPoqFlioyGSwCECCmhk703g6qIM4"
YOUR_SECRET_KEY_V3 = "6LfxELMpAAAAAAuTo365vfjgd_DpvsrDZQrV5znI"
GOOGLE_URL = 'https://www.google.com/recaptcha/api/siteverify'


class VerifyCaptcha(APIView):
    """Calls Google endpoint to verify front-end TOKEN and returns information whether user is a human.
    """
    # ...

        # This is POST endpoint that we were calling with axios in the first front-end example.
    def post(self, request, *args, **kwargs):
        # Decoding the payload
        request = json.loads(request.body.decode('utf-8'))
        # Taking out the token from the payload
        TOKEN_GENERATED_ON_FRONT_END_ACTION = request['token']
        VERSION = request['version']
        KEY = YOUR_SECRET_KEY_V3 if VERSION == 'V3' else YOUR_SECRET_KEY_V2
        # Creating body to send to Google for verification. You could also pass user's IP as an optional parameter but I never do that.
        body = {
            "secret": KEY,
            "response": TOKEN_GENERATED_ON_FRONT_END_ACTION
        }
        # Sending the request
        r = requests.post(GOOGLE_URL, data=body, json=body,)
        # Receiving the response
        google_response = r.json()
        print(google_response)
        print(google_response)
        print(google_response)
        # Analyzing the response
        if google_response['success'] == True:
            # Preparing our response that will be send to our front-end
            response = {"is_human": True}

            if VERSION == "V3":
                # This is our custom logic in case the request was initiated by a bot.
                if google_response['score'] < 0.5:
                    response['is_human'] = False
                return Response(
                    data=response, status=status.HTTP_200_OK, content_type="application/json")
            else:
                return Response(
                    data=response, status=status.HTTP_200_OK, content_type="application/json")
        else:
            return Response(
                data={"is_human": None, "message": "Validation of FE token went wront."}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

