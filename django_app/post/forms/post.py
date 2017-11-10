from django import forms

__all__ = (
    'SearchForm',
)

class SearchForm(forms.Form):
    search_item = forms.CharField(max_length=30,widget=forms.TextInput\
                                (attrs={'placeholder': '검색어를 입력하세요', 'id': 'search-btn'}))