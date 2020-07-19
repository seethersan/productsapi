from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from users.models import User

import json

@method_decorator(csrf_exempt, name='dispatch')
class Users(View):
    def get(self, request, *args, **kwargs):
        document_id = self.kwargs.get('document_id')
        if document_id:
            user = [user.attribute_values for user in self.query(document_id)]
            return JsonResponse({"user_information": user}, safe=False)
        else:
            users = [item.attribute_values for item in User.scan()]
            return JsonResponse({"users": users}, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        e = []
        try:
            new_user = User(**data)
            new_user.validate_user()
        except Exception as errors:
            for error in errors.args[0]:
                e.append(error.args[0])
                return JsonResponse(status=422, data={
                    "status": "ERROR",
                    "document_id": data['document_id'],
                    "errors": e
                }, safe=False)
        else:
            new_user.save()
            return JsonResponse(status=200, data={"status": "OK"})

@method_decorator(csrf_exempt, name='dispatch')
class UserInsert(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        error_users = []
        new_users = []
        parse_errors = 0
        users = data.get("users")
        if users:
            with User.batch_write() as batch:
                for user in users:
                    try:
                        new_user = User(**user)
                        new_user.validate_user()
                    except Exception as errors:
                        for error in errors.args[0]:
                            e.append(error.args[0])
                        error_users.append({
                            "document_id": user['document_id'],
                            "errors": e
                        })
                    except Exception:
                        parse_errors += 1
                    else:
                        new_users.append(new_user)
                if error_users or parse_errors:
                    return JsonResponse(status=422, data={
                        "status": "ERROR",
                        "users_report": error_users,
                        "number_of_users_unable_to_parse": parse_errors
                    }, safe=False)
                else:
                    for new_user in new_users:
                        batch.save(new_user)
                    return JsonResponse(status=200, data={"status": "OK"})