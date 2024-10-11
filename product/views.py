from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Brand, ProductType, SkinType

# Create your views here.
def home(request):
    return render(request, 'home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'product-list.html'
    context_object_name = 'products'
    paginate_by = 3  # Adjust as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply filters
        brand = self.request.GET.get('brand')
        product_type = self.request.GET.get('product_type')
        skin_type = self.request.GET.get('skin_type')

        if brand:
            queryset = queryset.filter(brand_id=brand)
        if product_type:
            queryset = queryset.filter(product_type_id=product_type)
        if skin_type:
            queryset = queryset.filter(suitable_skin_types__id=skin_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['product_types'] = ProductType.objects.all()
        context['skin_types'] = SkinType.objects.all()
        return context