import json

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.exceptions import ValidationError

from ads import settings
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
        self.object_list = self.object_list.select_related('category').select_related('author').order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get("page")
        page = paginator.get_page(page_num)

        result = [{
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author_id,
            'author': ad.author.first_name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category_id': ad.category_id,
            'image': ad.image.url if ad.image else None}
            for ad in page]
        response = {"items": result,
                    "total": paginator.count,
                    "num_pages": paginator.num_pages}
        return JsonResponse(response, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdEntityView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object = self.get_object()

        return JsonResponse({'id': self.object.id,
                             'name': self.object.name,
                             'author_id': self.object.author_id,
                             'author': self.object.author.first_name,
                             'price': self.object.price,
                             'description': self.object.description,
                             'is_published': self.object.is_published,
                             'category_id': self.object.category_id,
                             "category_name": self.object.category.name,
                             'image': self.object.image.url if self.object.image else None
                             })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Advertisement
    fields = ["name", "author_id", "price", "description", "category_id"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(get_user_model(), pk=data.get('author_id'))
        category = get_object_or_404(Category, pk=data.get('category_id'))

        ad = Advertisement.objects.create(
            name=data.get('name'),
            author=author,
            price=data.get('price'),
            description=data.get('description'),
            category=category,
            is_published=data.get('is_published')
        )

        ad.save()

        response = {'id': ad.id,
                    'name': ad.name,
                    'author_id': ad.author.id,
                    'author': ad.author.first_name,
                    'price': ad.price,
                    'description': ad.description,
                    'is_published': ad.is_published,
                    'category_id': ad.category_id,
                    'image': ad.image.url if ad.image else None
                    }

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Advertisement
    fields = ("name", "author", "price", "description", "category")

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.name = data.get('name')
        self.object.author = get_object_or_404(get_user_model(), pk=data.get('author_id'))
        self.object.price = data.get('price')
        self.object.description = data.get('description')
        self.object.category= get_object_or_404(Category, pk=data.get('category_id'))

        self.object.save()

        response = {'id': self.object.id,
                    'name': self.object.name,
                    'author_id': self.object.author.id,
                    'author': self.object.author.first_name,
                    'price': self.object.price,
                    'description': self.object.description,
                    'is_published': self.object.is_published,
                    'category_id': self.object.category.id,
                    "category_name": self.object.category.name,
                    'image': self.object.image.url if self.object.image else None
                    }
        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Advertisement
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(AdDeleteView, self).delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUploadView(UpdateView):
    model = Advertisement
    fields = ["name", "author", "price", "description", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object = self.get_object()

        image = request.FILE['image']
        self.object.image = image

        #self.object.author = get_object_or_404(get_user_model(), pk=self.object.author.id)
        #self.object.category = get_object_or_404(Category, pk=self.object.category.id)

        self.object.save()

        response = {'id': self.object.id,
                    'name': self.object.name,
                    'author_id': self.object.author.id,
                    'author': self.object.author.first_name,
                    'price': self.object.price,
                    'description': self.object.description,
                    'is_published': self.object.is_published,
                    'category_id': self.object.category.id,
                    "category_name": self.object.category.name,
                    'aimage': self.object.image.url if self.object.image else None
                    }
        return JsonResponse(response, status=200)
