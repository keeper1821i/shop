from random import randint

from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import FormView

from app_cart.forms import CartAddProductForm
from app_shop.forms import FilterForms, SortedForms, ReviewForms
from app_shop.models import Product, Reviews


def main_page(request):
    product_pieces_left = Product.objects.order_by('-quantity')[:5].select_related('category')
    product_number_of_sales = Product.objects.order_by('number_of_sales')[:8].select_related('category')
    number_1 = randint(14,24)
    random_product = Product.objects.filter(category_id__id__gte=number_1,
                                 category_id__id__lte=number_1+3)[:3].select_related('category')
    return render(request, 'static/index.html', {
                                                'product_pieces_left':product_pieces_left,
                                                'product_number_of_sales':product_number_of_sales,
                                                'random_product' : random_product,
                                                  })

def about_view(request):
    return render(request, 'static/about.html', {})


class ProductListView(generic.ListView):
    template_name = 'shop/catalog.html'
    model = Product
    context_object_name = 'catalog'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        form = FilterForms()
        form_sorted = SortedForms()
        context['form_sorted'] = form_sorted
        context['form'] = form
        return context

    def post(self,request):
        form = FilterForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if name:
                filter_product = Product.objects.filter(
                                                        name__icontains=name,
                                                        )
            price = form.cleaned_data.get('price')
            price = price.split(';')
            if price:
                filter_product = Product.objects.filter(price__gte=int(price[0]),
                                                        price__lte=int(price[1]),
                                                        )
            free_shipping = form.cleaned_data.get('free_shipping')
            if free_shipping:
                filter_product = Product.objects.filter(
                                                        free_delivery=free_shipping,
                                                        )

            available = form.cleaned_data.get('available')
            if available:
                filter_product = Product.objects.filter(
                                                        available=available
                                                        )


            return render(request, 'shop/catalog.html', {'filter_product': filter_product, 'form': form})
        else:
            return redirect('catalog/')


class CategoryDetail(generic.ListView):

    """ Отображение категорий """

    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'category_detail'

    def get_context_data(self, **kwargs):
        context = {}
        form = FilterForms()
        form_sorted = SortedForms()
        context['form_sorted'] = form_sorted
        context['form'] = form
        pk=self.kwargs['pk']
        sorted_product=Product.objects.filter(category_id=pk)
        context['sorted_product'] = sorted_product
        return context

    def post(self,request, pk):
        form = FilterForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if name:
                filter_product = Product.objects.filter(
                    name__icontains=name,
                    category_id=pk
                )
            price = form.cleaned_data.get('price')
            price = price.split(';')
            if price:
                filter_product = Product.objects.filter(price__gte=int(price[0]),
                                                        price__lte=int(price[1]),
                                                        category_id=pk
                                                        )
            free_shipping = form.cleaned_data.get('free_shipping')
            if free_shipping:
                filter_product = Product.objects.filter(
                    free_delivery=free_shipping,
                    category_id=pk
                )

            available = form.cleaned_data.get('available')
            if available:
                filter_product = Product.objects.filter(
                    available=available,
                    category_id=pk
                )

            return render(request, 'shop/catalog.html', {'filter_product': filter_product, 'form': form, 'pk': pk})
        else:
            return redirect(f'catalog/{pk}')


class SubCtegoryDetail(generic.ListView):

    """Отображение подкатегорий"""
    model = Product
    template_name = 'shop/catalog.html'
    context_object_name = 'subcategory_detail'

    def get_context_data(self, **kwargs):
        context = {}
        form = FilterForms()
        form_sorted = SortedForms()
        context['form_sorted'] = form_sorted
        context['form'] = form
        pk=self.kwargs['pk']
        sorted_product=Product.objects.filter(subcategory_id=pk)
        context['sorted_product'] = sorted_product
        return context

    def post(self,request, pk):
        form = FilterForms(request.POST)
        form_sorted = SortedForms(request.POST)
        if form_sorted.is_valid():
            price_sorted = form_sorted.cleaned_data.get('price')
            print(price_sorted)
        if form.is_valid():
            if form.is_valid():
                name = form.cleaned_data.get('name')
                if name:
                    filter_product = Product.objects.filter(
                        name__icontains=name,
                        subcategory_id=pk
                    )
                price = form.cleaned_data.get('price')
                price = price.split(';')
                if price:
                    filter_product = Product.objects.filter(price__gte=int(price[0]),
                                                            price__lte=int(price[1]),
                                                            subcategory_id=pk
                                                            )
                free_shipping = form.cleaned_data.get('free_shipping')
                if free_shipping:
                    filter_product = Product.objects.filter(
                        free_delivery=free_shipping,
                        subcategory_id=pk
                    )

                available = form.cleaned_data.get('available')
                if available:
                    filter_product = Product.objects.filter(
                        available=available,
                        subcategory_id=pk
                    )
            return render(request, 'shop/catalog.html', {'filter_product': filter_product, 'form': form})
        else:
            return redirect(f'/subcatalog/{pk}')


class ProductDetail(generic.DetailView, FormView):

    """Информация о продукте"""

    template_name = 'shop/product.html'
    context_object_name = 'product_detail'
    form_class = ReviewForms

    def get_queryset(self):
        return Product.objects.all().prefetch_related('product_review').select_related('category')

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        form_add_cart = CartAddProductForm()
        context['form_add_cart'] = form_add_cart
        result = Reviews.objects.filter(review_product__id=self.kwargs['pk']).select_related('author')
        count_review = Product.objects.filter(id = self.kwargs['pk']).annotate(product_reviews=Count('product_review__id'))
        count_review = count_review[0].product_reviews
        context['count_review'] = count_review
        context['result'] = result
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return f'/product_detail/{pk}'


    def form_valid(self, form):
        inst = Product.objects.filter(id=self.kwargs['pk'])
        body = form.cleaned_data.get('body')
        print(body)
        print(self.request.user.id)
        res = Reviews.objects.create(descriptions = body, author_id=self.request.user.id)
        res.review_product.set(inst)
        return super().form_valid(form)

