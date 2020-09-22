from django.shortcuts import render
from .helpers import predict, process_image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .serializers import ImageSerializer
from rest_framework import status
# Create your views here.
class PredictAPI(APIView):
    """
    This endpoint is for prediction.
    It has field named 'image'  which takes image url on post request.
    Returns Response with predicted disease.
    """
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
    """
    This endpoint is for image upload.
    It has a field named 'image' which takes image file on post request.
    Returns image url needed to predict.
    """
    parser_class = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=self.request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
