from django.shortcuts import render
from django.http import HttpResponse
# HttpResponseの代わりに、プロのウェイターである「render」をインポート 
from django.shortcuts import render 


def index(request):
    # シェフが料理（データ）を準備し、「context」というお盆に乗せる 
    # 'title'という名前の料理、「こんにちは、Django」という中身 
    context = {'title': 'こんにちは、Django', 'message': 'これはテンプレートを使ったテストページです。', 'food_list':['カレー', 'ラーメン', '寿司'], } 
    # ウェイター(render)を呼び出し、依頼書(request)とお皿(index.html)と料理(context)を渡す 
    return render(request, 'index.html', context)


# Create your views here