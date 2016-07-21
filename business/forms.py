from django import forms


class FacebookPageSearchForm(forms.Form):
    search_key = forms.CharField(max_length=200, required=True, initial='Business in HSR Layout, Bangalore')
    access_token = forms.CharField(
        max_length=200,
        required=True,
        help_text='Get access_token from <a href="https://developers.facebook.com/tools/explorer/145634995501895/" target="_blank">here</a>',
    )
