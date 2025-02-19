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
                created_by_name=F("created_by__username"),
                assigned_to_name=F("assigned_to__username")
            ).values(
                "id", "created_by_name", "assigned_to_name",
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

    def post(self, request):
        form = CreateKnownDiffModalForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            description = json.dumps({
                "issue_description": form_data.get("issue_description"),
                "behaviour1": form_data.get("behaviour1"),
                "behaviour2": form_data.get("behaviour2"),
                "fb": form_data.get("fb"),
                "model_mapping": form_data.get("model_mapping")
            })

            # creating Known Diff
            KnownDiff.objects.create(
                diff_name=form_data.get("diff_name"),
                rule_id=form_data.get("rule_id"),
                diff_url=form_data.get("diff_url"),
                raised_by=form_data.get("raised_by"),
                assigned_to=form_data.get("assigned_to"),
                description=description,
                created_by=request.user
            )
            return redirect('list_known_diff')
        else:
            return render(request, self.template_name, {'known_diff_form': form})


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


class DetailKnownDiffAPIView(APIView):
    permission_classes = [UserAuthentication]
    template_name = 'detail_known_diff.html'

    def get(self, request, pk):
        known_diff = KnownDiff.objects.filter(
            ~Q(is_active=3), id=pk
        ).first()

        known_diff_details = {}

        if known_diff:
            description = json.loads(known_diff.description) if known_diff.description else {}
            known_diff_details.update({
                **description,
                "diff_name": known_diff.diff_name,
                "diff_url": known_diff.diff_url,
                "rule_id": known_diff.rule_id,
                "raised_by_name": known_diff.raised_by.username if known_diff.raised_by else "",
                "assigned_to_name": known_diff.assigned_to.username if known_diff.assigned_to else ""
            })
        return render(request, self.template_name, {"known_diff_details": known_diff_details})


# class DeleteRecipeAPIView(APIView):
#     permission_classes = [UserAuthentication]

#     def get(self, request, pk):
#         user = request.user
#         Recipe.objects.filter(id=pk, author=user).update(is_active=False)
#         return redirect('list_recipe')
