import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.core.exceptions import ValidationError

from advertisements.models import Advertisement, Category


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsListView(ListView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        ads = self.object_list
        response = [{
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published, }
            for ad in ads]
        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        ad = Advertisement()
        data = json.loads(request.body)

        ad.name = data.get('name')
        ad.author = data.get('author')
        ad.price = data.get('price')
        ad.description = data.get('description')
        ad.address = data.get('address')
        ad.is_published = data.get('is_published')

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()

        return JsonResponse({'id': ad.id,
                            'name': ad.name,
                            'author': ad.author,
                            'price': ad.price,
                            'description': ad.description,
                            'address': ad.address,
                            'is_published': ad.is_published}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdEntityView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object = self.get_object()

        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author': self.object.author,
                             'price': self.object.price,
                             'description': self.object.description,
                             'address': self.object.address,
                             'is_published': self.object.is_published})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        cats = self.object_list
        response = [{'id': cat.id, "name": cat.name} for cat in cats]
        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        cat = Category()
        data = json.loads(request.body)

        cat.name = data.get('name')

        try:
            cat.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat.save()

        return JsonResponse({'id': cat.id, "name": cat.name}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryEntityView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({'id': self.object.id, "name": self.object.name})
