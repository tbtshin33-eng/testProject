# app/forms.py (新規作成) 
from django import forms 
from .models import Post 

class PostForm(forms.ModelForm): 
	class Meta: 
		model = Post
		fields = ['content'] 
		# ユーザーに入力してほしいフィールドを指定
