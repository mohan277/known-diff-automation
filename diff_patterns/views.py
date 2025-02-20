import datetime
import json

from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator

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
                "is_active", "rule_id", "diff_name", "created_at"
            )
        )
        # Number of objects per page
        per_page = request.GET.get('per_page', 10)  # Default is 10 if no per_page is specified
        paginator = Paginator(known_diffs, per_page)

        # Get the current page number from the request
        page_number = request.GET.get('page')
        known_diffs = paginator.get_page(page_number)
        return render(request, self.template_name, {"known_diffs": known_diffs, 'per_page': per_page})


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


class EditKnownDiffAPIView(APIView):
    permission_classes = [UserAuthentication]
    template_name = 'edit_known_diff.html'

    def get(self, request, pk):
        print("bjncjsncjscns", pk)
        form = CreateKnownDiffModalForm()
        known_diff = KnownDiff.objects.filter(
            ~Q(is_active=3), id=pk
        ).first()

        known_diff_details = {}
        if known_diff:
            description = json.loads(known_diff.description) if known_diff.description else {}
            known_diff_details.update({
                **description,
                "id": known_diff.id,
                "diff_name": known_diff.diff_name,
                "diff_url": known_diff.diff_url,
                "rule_id": known_diff.rule_id,
                "raised_by": known_diff.raised_by,
                "assigned_to": known_diff.assigned_to,
                "raised_by_name": known_diff.raised_by.username if known_diff.raised_by else "",
                "assigned_to_name": known_diff.assigned_to.username if known_diff.assigned_to else ""
            })

        return render(request, self.template_name, {'known_diff_form': form, "known_diff_details": known_diff_details})

    def post(self, request, pk):
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
            KnownDiff.objects.filter(id=pk).update(
                diff_name=form_data.get("diff_name"),
                rule_id=form_data.get("rule_id"),
                diff_url=form_data.get("diff_url"),
                raised_by=form_data.get("raised_by"),
                assigned_to=form_data.get("assigned_to"),
                description=description,
                updated_at=datetime.datetime.now()
            )
            return redirect('detail_known_diff', pk=pk)
        else:
            return render(request, self.template_name, {'known_diff_form': form})


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
                "id": known_diff.id,
                "diff_name": known_diff.diff_name,
                "diff_url": known_diff.diff_url,
                "rule_id": known_diff.rule_id,
                "raised_by_name": known_diff.raised_by.username if known_diff.raised_by else "",
                "assigned_to_name": known_diff.assigned_to.username if known_diff.assigned_to else ""
            })
        return render(request, self.template_name, {"known_diff_details": known_diff_details})


class DeleteKnownDiffAPIView(APIView):
    permission_classes = [UserAuthentication]

    def get(self, request, pk):
        user = request.user
        KnownDiff.objects.filter(id=pk, created_by=user).update(
            is_active=False, updated_at=datetime.datetime.now()
        )
        return redirect('list_known_diff')
