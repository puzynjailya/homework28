import json
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads import settings
from advertisements.models import Advertisement
from users.models import User, Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('username').annotate(total=Count('advertisement'))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num: int = request.GET.get('page')
        page = paginator.get_page(page_num)

        result: list = [{"id": user_page.id,
                         "username": user_page.username,
                         "first_name": user_page.first_name,
                         "last_name": user_page.last_name,
                         "role": user_page.role,
                         "age": user_page.age,
                         "locations": list(map(str, user_page.location.all())),
                         "total_ads": user_page.total}
                        for user_page in page]

        response: dict = {"items": result,
                          "total": paginator.count,
                          "num_pages": paginator.num_pages}

        return JsonResponse(response, safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        response = {"id": self.object.id,
                    "username": self.object.username,
                    "first_name": self.object.first_name,
                    "last_name": self.object.last_name,
                    "role": self.object.role,
                    "age": self.object.age,
                    "locations": list(map(str, self.object.location.all()))}

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = get_user_model()
    fields = ["username",
              "password",
              "first_name",
              "last_name",
              "role",
              "age",
              "location"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        new_user = get_user_model().objects.create(
            username=data.get('username'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role'),
            age=data.get('age')
        )
        for location in data.get('location'):
            loc, _ = Location.objects.get_or_create(location=location, defaults={"_is_active": "True"})
            new_user.location.add(loc)

        new_user.save()

        response = {"id": new_user.id,
                    "username": new_user.username,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                    "role": new_user.role,
                    "age": new_user.age,
                    "locations": list(map(str, new_user.location.all()))}

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = get_user_model()
    fields = ["username",
              "password",
              "first_name",
              "last_name",
              "role",
              "age",
              "location"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.username = data.get('username')
        self.object.password = data.get('password')
        self.object.first_name = data.get('first_name')
        self.object.last_name = data.get('last_name')
        self.object.role = data.get('role')
        self.object.age = data.get('age')

        for location in data.get('location'):
            loc, _ = Location.objects.get_or_create(location=location, defaults={"_is_active": "True"})
            get_user_model().location.add(loc)

        self.object.save()

        response = {"id": self.object.id,
                    "username": self.object.username,
                    "first_name": self.object.first_name,
                    "last_name": self.object.last_name,
                    "role": self.object.role,
                    "age": self.object.age,
                    "locations": list(map(str, self.object.location.all()))}

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = get_user_model()
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)

