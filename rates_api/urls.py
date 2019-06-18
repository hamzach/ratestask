from django.urls import path

from .views import AveragePriceView, AveragePriceWithNullView, UploadPriceView, UploadPriceUSDView


urlpatterns = [
    path('average_price/', AveragePriceView.as_view()),
    path('average_price_3_plus/', AveragePriceWithNullView.as_view()),
    path('upload_price_usd/', UploadPriceView.as_view()),
    path('upload_price_other/', UploadPriceUSDView.as_view()),
]
