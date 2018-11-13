# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from rest_framework.authtoken.models import Token
import base64
from api.models import *
import time
import json


# Create your views here.


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            try:
                password = base64.decodestring(password)[3:]
            except:
                password = ''

            user = auth.authenticate(username=username, password=password)
            if user:
                error_code = 0
                return JsonResponse({"error_code": 0, "uid": user.id})
            else:
                error_code = 10000
                return JsonResponse({"error_code": 10000})
        else:
            error_code = 10001
            status_code = 200
            return JsonResponse({"error_code": 10001})
    else:
        error_code = 10002
        status_code = 200
        return HttpResponse(status=400, content='{"msg":"请求方法类型错误"}', content_type='application/json')


def add_event(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        address = request.POST.get("address")
        meeting_time = request.POST.get("time")
        limit = request.POST.get("limit")
        status = request.POST.get("status")
        print status, type(status), status == '0'
        if title and address and meeting_time:
            meeting = Meeting.objects.filter(title=title)
            if meeting.exists():
                return JsonResponse({"error_code": 10002})
            if status not in ['0', '1', '2', '', None]:
                return JsonResponse({"error_code": 10003})
            try:
                meeting_timestamp = time.mktime(time.strptime(meeting_time, '%Y-%m-%d %H:%M:%S'))
            except:
                return JsonResponse({"error_code": 10010})
            if meeting_timestamp > time.time():
                if status == '' or status is None:
                    status = '0'
                meeting = Meeting.objects.create(title=title,
                                                 address=address,
                                                 time=meeting_time,
                                                 limit=limit,
                                                 status=int(status))
                return JsonResponse({"error_code": 0, "data": {"event_id": meeting.id, "status": meeting.status}})
        else:
            return JsonResponse({"error_code": 10001})
    else:
        return HttpResponse(status=400, content='{"msg":"请求方法类型错误"}', content_type='application/json')
    return HttpResponse("add_event")


def get_event_list(request):
    """查询会议记录"""
    if request.method == 'POST':
        title = request.POST.get("title")

        # title不传则返回全部会议记录，title传递后，根据title进行模糊查询
        if title:
            meetings = Meeting.objects.filter(title__contains=title)
        else:
            meetings = Meeting.objects.all()

        # 存在会议记录，则返回json，不存在，就返回error_code=10004
        if meetings.exists():
            meetings_dict = {"error_code": 0,
                             "event_list": []}
            print len(meetings), meetings
            for meeting in meetings:
                meetings_dict["event_list"].append({"id": meeting.id, "title": meeting.title, "status": meeting.status})
            meetings_json = json.dumps(meetings_dict)
            return HttpResponse(content_type="application/json", content=meetings_json)
        else:
            return JsonResponse({"error_code": 10004})
    else:
        return HttpResponse(status=400, content='{"msg":"请求方法类型错误"}', content_type='application/json')


def add_guest(request):
    if request.method == 'POST':
        event_id = request.POST.get("id")
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        if id and name and phone_number:
            meeting = Meeting.objects.filter(id=event_id)
            if meeting.exists():
                guest = Guest.objects.filter(phone_number=phone_number)
                if not guest.exists():
                    if len(Guest.objects.filter(meeting=meeting.first())) < meeting.first().limit:
                        guest = Guest.objects.create(name=name, phone_number=phone_number, email=email)
                        guest.meeting.add(meeting.first())
                        res = {
                            "error_code": 0,
                            "data": {
                                "event_id": meeting.first().id,
                                "guest_id": guest.id,
                            }
                        }
                        return JsonResponse(res)
                    else:
                        return JsonResponse({"error_code": 10006})
                else:
                    return JsonResponse({"error_code": 10005})

            else:
                return JsonResponse({"error_code": 10004})
        else:
            return JsonResponse({"error_code": 10001})
    else:
        return HttpResponse(status=400, content='{"msg":"请求方法类型错误"}', content_type='application/json')
