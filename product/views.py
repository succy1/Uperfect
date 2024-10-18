from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Product, Brand, ProductType, SkinType, UserProduct
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'product-list.html'
    context_object_name = 'products'
    paginate_by = 6  # Adjust as needed

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
    
def find_suitable_products(user_profile):
    # Get all product types
    product_types = ProductType.objects.all()
    
    # Get user's skin types, conditions, and goals
    user_skin_types = user_profile.skin_types.all()
    user_skin_conditions = user_profile.skin_conditions.all()
    user_skincare_goals = user_profile.skincare_goals.all()
    
    # Prepare a dictionary to store recommended products
    recommended_products = {}
    
    for product_type in product_types:
        # Filter products by product type and suitable skin types
        suitable_products = Product.objects.filter(
            product_type=product_type,
            suitable_skin_types__in=user_skin_types
        ).distinct()
        
        # Further filter products by skin conditions and skincare goals
        condition_goal_keywords = list(user_skin_conditions.values_list('condition_type', flat=True)) + \
                                  list(user_skincare_goals.values_list('goal', flat=True))
        
        condition_goal_query = Q()
        for keyword in condition_goal_keywords:
            condition_goal_query |= Q(description__icontains=keyword) | \
                                    Q(pros__icontains=keyword) | \
                                    Q(cons__icontains=keyword)
        
        suitable_products = suitable_products.filter(condition_goal_query)
        
        # Get top 5 products based on average rating
        top_products = suitable_products.order_by('-avg_rating')[:5]
        
        if top_products:
            recommended_products[product_type.name] = list(top_products)
    
    return recommended_products

def profile_creation_completed(request):
    user_profile = request.user.profile
    recommended_products = find_suitable_products(user_profile)
    
    return render(request, 'recommended_products.html', {'recommended_products': recommended_products})

@login_required
def assign_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user_product, created = UserProduct.objects.get_or_create(user=request.user, product=product)
        
        if created:
            return JsonResponse({'status': 'success', 'message': 'Product assigned successfully'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Product was already assigned'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)