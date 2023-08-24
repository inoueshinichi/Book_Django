from django.shortcuts import render

# Create your views here.
from django.views import generic

from django.urls import reverse_lazy # URLの逆引き
from django.contrib import messages # ブラウザで応答 ERROR/WARNING/SUCCESS/INFO
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン状態でないとアクセスできない仕組みを持つクラス

# forms
from .forms import InquiryForm

# models
from .models import Diary

import logging
logger = logging.getLogger(__name__)


# 初期画面
class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
# 問い合わせ画面
class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    # override
    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
    
# 日記画面
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries
    
