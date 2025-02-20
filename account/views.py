from django.db.models import Count
from rest_framework.views import APIView
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .models import Users
from .forms import LoginModalForm, SignUpModalForm
from core.api_permissions import UserAuthentication
from core.encryption import jwt_encode_handler, jwt_payload_handler


class LoginAPIView(APIView):
    template_name = 'login.html'

    def get(self, request):
        form = LoginModalForm()
        return render(request, self.template_name, context={'login_form': form})

    def post(self, request):
        form = LoginModalForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = Users.objects.filter(username=username).first()
            if user:
                # Generate a JWT token with the user ID as the payload
                token = jwt_encode_handler((jwt_payload_handler(user)))
                # Store the token in a cookie or local storage
                response = redirect('list_known_diff')
                response.set_cookie("token", token)
                return response
        else:
            return render(request, self.template_name, {'login_form': form})


class SignUpAPIView(APIView):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpModalForm()
        return render(request, self.template_name, context={'signup_form': form})

    def post(self, request):
        form = SignUpModalForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # creating new user
            user_obj = Users.objects.create(username=username)
            user_obj.password = make_password(password)
            user_obj.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {'signup_form': form})


# class DashboardAPIView(APIView):
#     permission_classes = [UserAuthentication]
#     template_name = 'dashboard.html'

#     def get(self, request):
#         # Extract counts for veg and non-veg
#         veg_count = Recipe.objects.filter(author=request.user, meal_type="vegetarian", is_active=True).count()
#         non_veg_count = Recipe.objects.filter(author=request.user, meal_type="non_vegetarian", is_active=True).count()
        
#         veg_percentage = 0
#         non_veg_percentage = 0
#         if veg_count + non_veg_count > 0:
#             veg_percentage = round((veg_count/(veg_count+non_veg_count))*100, 2)
#             non_veg_percentage = round((non_veg_count/(veg_count+non_veg_count))*100, 2)
#         context = {
#             "chart_data": {
#                 "veg_percentage": veg_percentage,
#                 "non_veg_percentage": non_veg_percentage
#             }
#         }
#         return render(request, self.template_name, context)


# class CreateRecipeAPIView(APIView):
#     permission_classes = [UserAuthentication]
#     template_name = 'create_recipe.html'

#     def get(self, request):
#         recipes = list(Recipe.objects.filter(author=request.user, is_active=True).values())
#         return render(request, self.template_name, {"recipes": recipes})


class LogoutAPIView(APIView):
    def get(self, request):
        response = redirect("login")
        response.delete_cookie("token")
        return response
