import datetime
import json

from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.db.models import Q, F

from diff_patterns.models import KnownDiff
from .forms import CreateKnownDiffModalForm
from core.api_permissions import UserAuthentication


class ListKnownDiffAPIView(APIView):
    permission_classes = [UserAuthentication]
    template_name = 'list_known_diff.html'

    def get(self, request):
        known_diffs = list(
            KnownDiff.objects.filter(~Q(is_active=3)).annotate(
                created_by_name=F("created_by__username")
            ).values(
                "id", "created_by_name",
                "is_active", "rule_id", "diff_name"
            )
        )
        return render(request, self.template_name, {"known_diffs": known_diffs})


class CreateKnownDiffAPIView(APIView):
    permission_classes = [UserAuthentication]
    template_name = 'create_known_diff.html'

    def get(self, request):
        form = CreateKnownDiffModalForm()
        return render(request, self.template_name, {"known_diff_form": form})

    # def post(self, request):
    #     form = CreateKnownDiffModalForm(request.POST)
    #     if form.is_valid():
    #         form_data = form.cleaned_data
    #         KnownDiff.objects.create(
    #             author=request.user,
    #             **form_data
    #         )
    #         return redirect('list_recipe')
    #     else:
    #         return render(request, self.template_name, {'recipe_form': form})


# class EditRecipeAPIView(APIView):
#     permission_classes = [UserAuthentication]
#     template_name = 'edit_recipe.html'

#     def get(self, request, pk):
#         form = CreateRecipeModalForm()
#         recipe_obj = Recipe.objects.filter(id=pk).first()
#         return render(request, self.template_name, {'recipe_form': form, "recipe_obj": recipe_obj})

#     def post(self, request, pk):
#         form = CreateRecipeModalForm(request.POST)
#         if form.is_valid():
#             form_data = form.cleaned_data
#             Recipe.objects.filter(id=pk).update(
#                 **form_data, updated_at=datetime.datetime.now()
#             )
#             return redirect('list_recipe')
#         else:
#             return render(request, self.template_name, {'recipe_form': form})


# class DetailRecipeAPIView(APIView):
#     permission_classes = [UserAuthentication]
#     template_name = 'detail_recipe.html'

#     def get(self, request, pk):
#         recipe_obj = Recipe.objects.filter(id=pk).first()

        # for known_diff in known_diffs:
        #     if known_diff.get("description"):
        #         known_diff["description"] = json.loads(known_diff["description"])
        #     if known_diff.get("diff_data"):
        #         known_diff["diff_data"] = json.loads(known_diff["diff_data"])
        # print("#"*100)
        # print(known_diffs)
        # print("#"*100)
#         return render(request, self.template_name, {"recipe_obj": recipe_obj})


# class DeleteRecipeAPIView(APIView):
#     permission_classes = [UserAuthentication]

#     def get(self, request, pk):
#         user = request.user
#         Recipe.objects.filter(id=pk, author=user).update(is_active=False)
#         return redirect('list_recipe')
