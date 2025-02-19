from django import forms

from diff_patterns.models import KnownDiff
from account.models import Users


class CreateKnownDiffModalForm(forms.ModelForm): 
    issue_description = forms.CharField(
        max_length=1000, 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # Multi-line input
        help_text="Enter up to 1000 characters."
    )
    behaviour1 = forms.CharField(
         max_length=1000, 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # Multi-line input
        help_text="Enter up to 1000 characters."
    )
    behaviour2 = forms.CharField(
         max_length=1000, 
        required=False, 
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # Multi-line input
        help_text="Enter up to 1000 characters."
    )
    fb = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter up to 255 characters."
    )
    model_mapping = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter up to 255 characters."
    )

    class Meta:
        model = KnownDiff
        fields = (
            "diff_name", "rule_id", "diff_url", "diff_data",
            "diff_image", "assigned_to", "raised_by"
        )

    def __init__(self, *args, **kwargs):
        super(CreateKnownDiffModalForm, self).__init__(*args, **kwargs)
        users = Users.objects.filter(is_active=True)
        self.fields['assigned_to'].queryset = users
        self.fields['assigned_to'].empty_label = "Select Assignee"
        
        self.fields['raised_by'].queryset = users
        self.fields['raised_by'].empty_label = "Raised for"

    def clean(self):
        cleaned_data = super().clean()
        issue_description = cleaned_data.get("issue_description")
        behaviour1 = cleaned_data.get("behaviour1")
        behaviour2 = cleaned_data.get("behaviour2")
        fb = cleaned_data.get("fb")
        model_mapping = cleaned_data.get("model_mapping")

        if issue_description and len(issue_description) > 1000:
            self.add_error("issue_description", "Comment should not exceed 1000 characters.")
        if behaviour1 and len(behaviour1) > 1000:
            self.add_error("behaviour1", "Comment should not exceed 1000 characters.")
        if behaviour2 and len(behaviour2) > 1000:
            self.add_error("behaviour2", "Comment should not exceed 1000 characters.")
        if fb and len(fb) > 255:
            self.add_error("fb_data", "Comment should not exceed 255 characters.")
        if model_mapping and len(model_mapping) > 255:
            self.add_error("fb_data", "Comment should not exceed 255 characters.")

        return cleaned_data
