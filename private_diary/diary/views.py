from django.shortcuts import render

# Create your views here.
from django.views import generic

from django.urls import reverse_lazy # URLの逆引き
from django.contrib import messages # ブラウザで応答 ERROR/WARNING/SUCCESS/INFO

from .forms import InquiryForm

import logging
logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
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
