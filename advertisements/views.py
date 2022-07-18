import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.exceptions import ValidationError

from advertisements.models import Advertisement
from categories.models import Category
from users.models import User


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
class AdCreateView(CreateView):
    model = Advertisement
    fields = []

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        author = get_object_or_404(User, pk=data.get('author_id'))
        category = get_object_or_404(Category, pk=data.get('category_id'))

        ad = Advertisement.objects.create(
            name=data.get('name'),
            author=author,
            price=data.get('price'),
            description=data.get('description'),
            category=category,
            is_published=data.get('is_published')
            )

        response = {'id': ad.id,
                    'name': ad.name,
                    'author_id': ad.author,
                    'author': ad.author.first_name,
                    'price': ad.price,
                    'description': ad.description,
                    'is_published': ad.is_published,
                    'category_id': ad.category_id,
                    'image': ad.image
                    }

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Advertisement
    fields = ["name", "author_id", "price", "description", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.name = data.get('name')
        self.object.author = get_object_or_404(User, pk=data.get('author_id'))
        self.object.price = data.get('price')
        self.object.description = data.get('description')
        self.object.category = get_object_or_404(Category, pk=data.get('category_id'))

        self.object.save()

        response = {'id': self.object.id,
                    'name': self.object.name,
                    'author_id': self.object.author,
                    'author': self.object.author.first_name,
                    'price': self.object.price,
                    'description': self.object.description,
                    'is_published': self.object.is_published,
                    'category_id': self.object.category_id,
                    'image': self.object.image
                    }
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Advertisement
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(AdDeleteView, self).delete(request, *args, **kwargs)

        return JsonResponse({"status":"ok"}, status=200)