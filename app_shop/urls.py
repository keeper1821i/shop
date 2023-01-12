from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app_shop.views import main_page, CategoryDetail, ProductDetail, SubCtegoryDetail, ProductListView, about_view

urlpatterns = [
    path('', main_page, name='main_page'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('catalog/<int:pk>', CategoryDetail.as_view(), name='catalog_detail'),
    path('product_detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('subcatalog/<int:pk>', SubCtegoryDetail.as_view(), name='subcategory_detail'),
    path('about/', about_view, name='about')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
