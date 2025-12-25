from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Post
from django.shortcuts import redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy 
from django.views.generic import CreateView 
from django.contrib.auth.forms import UserCreationForm 
from .serializers import PostSerializer 
import requests



def timeline(request): 
    query = request.GET.get('q')
    if query:
        # もしクエリがあれば、contentにその文字列を含む投稿をフィルタリング
        posts = Post.objects.filter(content__icontains=query).order_by('-created_at')
    else:
        # クエリがなければ、全ての投稿を表示
        posts = Post.objects.select_related('author').order_by('-created_at')


	# 2. 取得したデータをテンプレートに渡す準備
    context = {
    		'posts': posts,
            'query': query,
	}

	# 3. テンプレートを呼び出し、データを渡して表示する
    return render(request, 'timeline.html', context)


def post_detail(request, pk):
    # pkを使って、Postオブジェクトを1件だけ取得する 
    # 存在しない場合は404エラーを返す 
    post = get_object_or_404(Post, pk=pk) 
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create(request):
    # 1. POSTリクエスト（送信ボタン押下時）の処理
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() 
            print("初めのprint文")
            print("投稿者： " + post.author)
            print("投稿文：" + str(post.content))
            print("最後のprint文")
            return redirect('timeline') 
        # (POSTで無効だった場合は、下の 'return render' に進む)
    
    # 2. GETリクエスト（ページ初回表示時）の処理
    else:
        form = PostForm() # 空のフォームを作成

    # 3. GETリクエスト、または POSTが失敗した場合
    return render(request, 'post_create.html', {'form': form})

def post_edit(request, pk): 
    post = get_object_or_404(Post, pk=pk) # 権限チェック：投稿者とログインユーザーが一致しない場合はリダイレクト 
    if request.user != post.author: 
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        # 既存のインスタンスを渡してフォームを生成
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
     # 既存のインスタンスを渡してフォームを生成（初期表示）
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})

def post_delete(request, pk): 
    post = get_object_or_404(Post, pk=pk) 
    if request.user != post.author: 
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete() # データを削除
        return redirect('timeline') # タイムラインにリダイレクト

    return render(request, 'post_confirm_delete.html', {'post': post})

class SignUpView(CreateView): 
    pｒint("signupの呼び出し")
    form_class = UserCreationForm 
    success_url = reverse_lazy('login') # 登録成功後はログインページへ 
    template_name = 'signup.html'

from rest_framework import generics
#Postモデルの一覧を返す、API専門のクラスベースビュー
class PostListAPIView(generics.ListAPIView): 
    # どのデータの一覧を返すか 
    queryset = Post.objects.all() 
    # どの翻訳者（シリアライザ）を使ってJSONに変換するか 
    serializer_class = PostSerializer

def weather(request):
   # 1. 都市と座標の辞書を定義   
   locations = {
       'Kanazawa': {'lat': 36.59, 'lon': 136.60},
        'Tokyo':    {'lat': 35.68, 'lon': 139.76},
        'Osaka':    {'lat': 34.69, 'lon': 135.50},
        'Sapporo':  {'lat': 43.06, 'lon': 141.35},
        'Naha':     {'lat': 26.21, 'lon': 127.68},
    }
   city_name = 'Kanazawa'
   if request.GET.get('city') and request.GET.get('city') in locations:
        city_name = request.GET.get('city')

   lat = locations[city_name]['lat']
   lon = locations[city_name]['lon']

    # 4. APIへのリクエストURLを作成
   api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'

 # 5. requestsを使ってデータを取得
   response = requests.get(api_url)
   data = response.json()

    # 6. テンプレートに渡すデータを作成
   context = {
        'city': city_name,
        'temperature': data['current_weather']['temperature'],
        'windspeed': data['current_weather']['windspeed'],
        # 天気コード(WMO code)。0=晴天, 1-3=曇り, 61-65=雨 など
        'weathercode': data['current_weather']['weathercode'],
    }

   return render(request, 'weather.html', context)
