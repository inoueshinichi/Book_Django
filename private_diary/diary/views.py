from django.shortcuts import render

# Create your views here.
from django.views import generic

from django.urls import reverse_lazy # URLの逆引き
from django.contrib import messages # ブラウザで応答 ERROR/WARNING/SUCCESS/INFO
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン状態でないとアクセスできない仕組みを持つクラス

# forms
from .forms import InquiryForm
from .forms import DiaryCreateForm

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
    # SQLの入口 (O/Rマッピングクラス)
    model = Diary

    # テンプレートHTML
    template_name = 'diary_list.html'

    # ページネイション(ページ移動などを簡単に行うためのUI部品.)
    # ListViewには, デフォルトで機能が備わっている.
    # テンプレート diary_list.htmlには, 現在のページオブジェクトとして「object_list」が送信される
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries
    
# 日記詳細画面
class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    # O/Rマッピング
    model = Diary

    # テンプレートHTML
    template_name = 'diary_detail.html'

    # キャプチャ変数名の変更
    # pk_url_kwarg = 'id' # `pk`->`id`


# 日記作成画面
class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    # O/Rマッピング
    model = Diary

    # テンプレートHTML
    template_name = 'diary_create.html'

    # フォーム
    form_class = DiaryCreateForm

    # 正常終了した際の遷移先ページを指定
    success_url = reverse_lazy('diary:diary_list') # 日記画面に戻る

    # override
    def form_valid(self, form):
        """検証を通過した場合に呼ばれる関数

        Args:
            form (_type_): _description_

        Returns:
            _type_: _description_
        """

        # フォームオブジェクトに格納した各変数をDBに保存しない(一時待機)
        diary = form.save(commit=False)
        diary.user = self.request.user # ログイン中のユーザー
        diary.save() # フォーム内部の各変数をDBに保存
        messages.success(self.request, '日記を作成しました')
        
        return super().form_valid(form)
    
    # override
    def form_invalid(self, form):
        """検証に不合格の場合に呼ばれる関数

        Args:
            form (_type_): _description_

        Returns:
            _type_: _description_
        """

        messages.error(self.request, "日記の作成に失敗しました")
        
        return super().form_invalid(form)

# 日記編集画面
class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    # O/Rマッピング
    model = Diary

    # テンプレートHTML
    template_name = 'diary_update.html'

    # フォーム
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '日記の更新に失敗しました')
        return super().form_invalid(form)
    

# 日記削除画面
class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    # O/Rマッピング
    model = Diary

    # テンプレートHTML
    template_name = 'diary_delete.html'

    # 遷移先画面
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました")
        return super().delete(request, *args, **kwargs)
    
    