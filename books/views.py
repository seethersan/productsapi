from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from books.models import Book

import json

@method_decorator(csrf_exempt, name='dispatch')
class Books(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        if id:
            book = [book.attribute_values for book in self.query(id)]
            return JsonResponse({"user_information": book}, safe=False)
        else:
            books = [item.attribute_values for item in Book.scan()]
            return JsonResponse({"books": books}, safe=False)
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        e = []
        try:
            new_book = Book(**data)
            new_book.validate_book()
        except Exception as e:
            for error in errors.args[0]:
                e.append(error.args[0])
                return JsonResponse(status=422, data={
                    "status": "ERROR",
                    "document_id": data['id'],
                    "errors": e
                }, safe=False)
        else:
            new_book.save()
            return JsonResponse(status=200, data={"status": "OK"})