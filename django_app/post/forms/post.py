from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from post.models import Post

__all__ = (
    'SearchForm',
)


class SearchForm(forms.Form):
    search_item = forms.CharField(max_length=30, widget=forms.TextInput \
        (attrs={'placeholder': '검색어를 입력하세요', 'id': 'search-btn'}))


class PostRegist(forms.ModelForm):
    image_1 = forms.ImageField(required=True, error_messages={'invalid': _("Image files only")},
                               widget=forms.FileInput(
                                   attrs={'class': 'file-upload__input', 'onchange': "upload_img(this,1);"}))
    image_2 = forms.ImageField(required=False, error_messages={'invalid': _("Image files only")},
                               widget=forms.FileInput(
                                   attrs={'class': 'file-upload__input', 'onchange': "upload_img(this,2);"}))
    image_3 = forms.ImageField(required=False, error_messages={'invalid': _("Image files only")},
                               widget=forms.FileInput(
                                   attrs={'class': 'file-upload__input', 'onchange': "upload_img(this,3);"}))
    Sell = 's'
    Buy = 'b'
    SELL_OR_BUY_CHOICE = {
        (Sell, 'Sell'),
        (Buy, 'Buy'),
    }
    electronics = 'e'
    fashion_cloths = 'fc'
    fashion_goods = 'fg'
    cosmetics_beauty = 'cb'
    sport = 's'
    book = 'b'
    CATEGORY_CHOICE = (
        (electronics, '전자기기'),
        (fashion_cloths, '패션의류'),
        (fashion_goods, '패션잡화'),
        (cosmetics_beauty, '화장품/미용'),
        (sport, '스포츠/레저'),
        (book, '도서'),
    )
    sell_or_buy = forms.ChoiceField(label_suffix='', choices=SELL_OR_BUY_CHOICE)
    category = forms.ChoiceField(label_suffix='', choices=CATEGORY_CHOICE)

    class Meta:
        model = Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mat-input'}),
            'price': forms.TextInput(attrs={'class': 'mat-input', 'type': 'number', 'min': '0', 'max': '1000000000'}),
            'content': forms.Textarea(attrs={'placeholder': 'content'}),
        }
        fields = ['title', 'category', 'sell_or_buy', 'price', 'content', 'image_1', 'image_2', 'image_3']

    def clean_price(self):
        price = int(self.cleaned_data.get("price"))
        if price < 0:
            forms.ValueError("0 이상의 수를 입력하세요.")
        return price

class PostUpdate(PostRegist):
    image_1 = forms.ImageField(required=False, error_messages={'invalid': _("Image files only")},
                               widget=forms.FileInput(
                                   attrs={'class': 'file-upload__input', 'onchange': "upload_img(this,1);"}))