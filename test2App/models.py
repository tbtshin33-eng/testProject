# app/models.py
from django.db import models
from django.contrib.auth.models import User # Django組み込みのUserモデルをインポート

class Post(models.Model):
    # 投稿内容：文字数制限のないテキストフィールド
    content = models.TextField()

    # 投稿日時：データが作成された時に自動で日時を記録
    created_at = models.DateTimeField(auto_now_add=True)

    # 投稿者：Userモデルと「一対多」の関係で紐づける
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # 管理画面などで見やすいように、オブジェクトの文字列表現を定義
        return f'{self.author.username}: {self.content[:20]}'
    
class Category(models.Model):
    
    name = models.CharField(max_length=31, verbose_name="カテゴリ名")

    def __str__(self):
        return self.name

    class Meta:

        verbose_name_plural = "カテゴリ"


class Article(models.Model):

    title = models.CharField(max_length=62, verbose_name="タイトル")
    slug = models.SlugField(verbose_name="URLスラッグ（英語）")
    image = models.ImageField(upload_to="article_image", blank=True, verbose_name="記事のイメージ写真", help_text="登録しない場合は、デフォルトのイメージ写真を使用する")
    categories = models.ManyToManyField(Category, verbose_name="カテゴリ")
    body = models.TextField(verbose_name="本文")
    status = models.PositiveSmallIntegerField(default=1, verbose_name="公開ステータス", help_text="1:下書き, 2:公開")
    liked = models.IntegerField(default=0, verbose_name="いいね数")
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")
    creator = models.CharField(max_length=31, verbose_name="投稿者")
    created = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")
    modified = models.DateTimeField(auto_now=True, verbose_name="更新日")

    def __str__(self):
        return self.title

    class Meta:
        
        verbose_name_plural = "記事"
    


class Comment(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="記事", related_name="comments")
    commenter = models.CharField(max_length=31, verbose_name="コメント者名")
    body = models.TextField(verbose_name="コメント文")
    created = models.DateTimeField(auto_now_add=True, verbose_name="コメント投稿日時")

    def __str__(self):
        return self.article.title + ":{}のコメント".format(self.commenter)

    class Meta:
        verbose_name_plural = "コメント"