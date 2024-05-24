from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.response import Response
from rest_framework import status
import requests



class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DestinationViewSet(ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class AvailableDestinations(APIView):
    
    def get(self,request):
        id = request.query_params.get('id')
        try:
            acc = Account.objects.get(id=id)
        except:
            return Response({'msg':'Account does not exist'},status=status.HTTP_400_BAD_REQUEST)
        dest = Destination.objects.filter(account=acc)
        serializer = DestinationSerializer(dest, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK )


class DataRecievingAPI(APIView):
    def post(self,request):
        if request.content_type != 'application/json':
            return Response({'msg':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        
        secret_token = request.headers.get('CL-X-TOKEN')
        print(request.headers)
        print(secret_token)
        if not secret_token:
            return Response({'msg':'Un Authenticate'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = Account.objects.get(app_secret_token = secret_token)
        except:
            return Response({'msg':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        for destination in Destination.objects.filter(account=account):
            method = destination.http_method
            url = destination.url
            headers = destination.headers

            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, params=data)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=data)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=data)
            except:
                print(f'failed url = {url},code = {response.status_code}')
                # return Response({'msg':'Sending Failed'},status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg':'Completed Successfully'},status=status.HTTP_200_OK)