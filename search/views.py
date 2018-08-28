from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from AuTomtit.WebCrawler.SearchEngine.ThePirateBay import ThePirateBay
# from AuTomtit.WebCrawler.SearchEngine.EZTV import EZTV


class SearchForm(forms.Form):
    key_words = forms.CharField(label="key-words", required=True, max_length=500)


class ResultPageForm(forms.Form):
    key_words = forms.CharField(label="key-words", required=True, max_length=500)


class ResultSplitForm(forms.Form):
    key_words = forms.CharField(label="key-words", required=True, max_length=500)
    page = forms.IntegerField(label="page")


class Search:
    search_engine = ThePirateBay()
    search_engine_iter = None

    @classmethod
    def search(cls, request):
        form = SearchForm(request.GET)
        if form.is_valid():
            key_words = form.cleaned_data['key_words']
            context = {
                'name': key_words,
            }
            return render(request, '../templates/search.html', context)
        else:
            return HttpResponseRedirect('/')

    @classmethod
    def result_page(cls, request):
        form = ResultPageForm(request.GET)
        if form.is_valid():
            key_words = form.cleaned_data['key_words']
            try:
                cls.search_engine.search(key_words)
                cls.search_engine_iter = cls.search_engine.results()
            except Exception as e:
                print(e)
                return HttpResponse('<h2>Web error.</h2>')
            context = {
                'name': key_words,
                'number': 10,
            }
            return render(request, '../templates/result_page.html', context)
        else:
            return HttpResponse('<h2>Input error.</h2>')

    @classmethod
    def result_split(cls, request):
        form = ResultSplitForm(request.GET)
        if form.is_valid():
            results = []
            try:
                for i, each in enumerate(cls.search_engine_iter):
                    if i < 10:
                        results.append(each)
                    else:
                        break
            except Exception as e:
                print(e)
                return HttpResponse('<h2>Parse error.</h2>')
            context = {
                'results': results,
            }
            return render(request, '../templates/result_split.html', context)
        else:
            return HttpResponse('<h2>Input error.</h2>')
