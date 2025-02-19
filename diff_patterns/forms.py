from django import forms

from diff_patterns.models import KnownDiff
from account.models import Users


class CreateKnownDiffModalForm(forms.ModelForm):
    class Meta:
        model = KnownDiff
        fields = (
            "diff_name", "rule_id", "description",
            "diff_url", "diff_data", "diff_image",
            "assigned_to", "raised_by"
        )

    def __init__(self, *args, **kwargs):
        super(CreateKnownDiffModalForm, self).__init__(*args, **kwargs)
        users = Users.objects.filter(is_active=True)
        self.fields['assigned_to'].queryset = users
        self.fields['assigned_to'].empty_label = "Select Assignee"
        
        self.fields['raised_by'].queryset = users
        self.fields['raised_by'].empty_label = "Raised for"
