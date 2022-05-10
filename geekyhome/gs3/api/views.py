from rest_framework import status
from functools import partial
import json
from django.shortcuts import render
import io
from .serializers import StudentSerializer
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
# Create your views here.

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        json_data =request.body
        stream = io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id= pythondata.get('id',None)
        if id is not None:
            stu =Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data =JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='application/json')
        stu = Student.objects.all()
        serializer = StudentSerializer(stu,many=True)
        json_data= JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
    if request.method == 'POST':
        print("called post method")
        json_data = request.body
        stream = io.BytesIO(json_data)
        print("iam stream")
        pythondata =JSONParser().parse(stream)
        serializer=StudentSerializer(data=pythondata)
        print(pythondata)
        if serializer.is_valid():
            print("iam valid")
            serializer.save()
            res = {'msg':'Data Created'}
            print(res)
            json_data= JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
    
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata =JSONParser().parse(stream)
        id=pythondata.get('id')
        stu= Student.objects.get(id=id)
        serializer=StudentSerializer(stu,data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data Updated'}
            json_data= JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata =JSONParser().parse(stream)
        id=pythondata.get('id')
        stu= Student.objects.get(id=id)
        stu.delete()
        res = {'msg':'Data Deleted'}
        json_data= JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    data ={
        'name':'nakula',
        'roll':15,
        'city':'ay'
    }
    print("tutoriallist is called")
    if request.method == 'POST':
        print("iam in post method",request)
        json_data = request.body
        print("jsond_ata",json_data)
        stream = io.BytesIO(json_data)
        print("iam stream",stream)
        pythondata =JSONParser().parse(stream)
        print("pythondata",pythondata)
        serializer = StudentSerializer(data=pythondata)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)