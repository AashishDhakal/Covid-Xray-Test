from django.shortcuts import render
from .helpers import predict, process_image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .serializers import ImageSerializer
from rest_framework import status
# Create your views here.
class PredictAPI(APIView):

    def post(self, request, *args, **kwargs):
        image = request.POST.get('image', False)
        array = process_image(image)
        result = predict(array)
        if result==0:
            return Response({
                'status': True,
                'prediction': 'COVID 19'
            })
        elif result==1:
            return Response({
                'status': True,
                'prediction': 'Normal'
            })
        elif result==2:
            return Response({
                'status': True,
                'prediction': 'Viral Pneumonia'
            })
        else:
            return Response({
                'status': False,
                'prediction': 'Unknown'
            })


class ImageUpload(APIView):
    parser_class = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=self.request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
