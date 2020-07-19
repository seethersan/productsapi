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
            return JsonResponse({"book_information": book}, safe=False)
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

@method_decorator(csrf_exempt, name='dispatch')
class BookInsert(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        error_books = []
        new_books = []
        parse_errors = 0
        books = data.get("books")
        if books:
            with Book.batch_write() as batch:
                for book in books:
                    try:
                        new_book = Book(**book)
                        new_book.validate_book()
                    except ValidationError as errors:
                        for error in errors.args[0]:
                            e.append(error.args[1])
                        error_books.append({
                            "product_id": new_product.id,
                            "errors": e
                        })
                    except Exception:
                        parse_errors += 1
                    else:
                        new_books.append(new_product)
                if error_books or parse_errors:
                    return JsonResponse(status=422, data={
                        "status": "ERROR",
                        "books_report": error_books,
                        "number_of_books_unable_to_parse": parse_errors
                    }, safe=False)
                else:
                    for new_book in new_books:
                        batch.save(new_book)
                    return JsonResponse(status=200, data={"status": "OK"})