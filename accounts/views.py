from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .quiz import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.apps import apps
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json
from .decorators import subscription_required

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f"Tài khoản của bạn đã được tạo!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def skin_quiz(request):
    return render(request, 'skin-quiz.html', {'questions': SKIN_QUIZ})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    UserProduct = apps.get_model('product', 'UserProduct')
    Review = apps.get_model('product', 'Review')

    user_products = UserProduct.objects.filter(user=request.user).select_related('product')
    user_reviews = Review.objects.filter(user=request.user).select_related('product')

    grouped_user_products = {}
    for user_product in user_products:
        product_type = user_product.product.product_type.name
        if product_type not in grouped_user_products:
            grouped_user_products[product_type] = []
        grouped_user_products[product_type].append(user_product)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    skin_type_idx = profile.skin_types.all().values_list("id", flat=True)
    skincare_advice = SkincareAdvice.objects.filter(skin_type_id__in=skin_type_idx)

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    checkins = DailyCheckIn.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # Prepare data for charts
    chart_data = {
        'dates': [checkin.date.strftime('%Y-%m-%d') for checkin in checkins],
        'composite_scores': [checkin.calculate_composite_score() for checkin in checkins],
        'sleep_scores': [checkin.calculate_sleep_score() for checkin in checkins],
        'stress_scores': [checkin.calculate_stress_score() for checkin in checkins],
        'skin_scores': [checkin.calculate_skin_feel_score() for checkin in checkins]
    }
    
    # Calculate weekly stats
    weekly_stats = {}
    if checkins:
        weekly_stats = {
            'blemish_percentage': sum(1 for c in checkins if c.new_blemishes) / len(checkins) * 100,
            'avg_sleep': sum(float(c.sleep_hours) for c in checkins) / len(checkins),
            'avg_stress': sum(c.stress_level for c in checkins) / len(checkins),
            'skincare_consistency': sum(1 for c in checkins if c.used_skincare) / len(checkins) * 100,
            'avg_composite_score': sum(c.calculate_composite_score() for c in checkins) / len(checkins)
        }

    context = {
        'profile': profile,
        'user_products': grouped_user_products,
        'user_reviews': user_reviews,
        'u_form': u_form,
        'p_form': p_form,
        'skincare_advice': skincare_advice,
        'chart_data': json.dumps(chart_data),
        'weekly_stats': weekly_stats,
        'has_checkins': bool(checkins)
    }

    return render(request, 'profile.html', context)

@login_required
def onboarding(request):
    # try:
    #     if hasattr(request.user, 'profile') and request.user.profile:
    #         return redirect('profile')
    # except Profile.DoesNotExist:
    #     pass

    if request.method == 'POST':
        step = request.POST.get('step')
        
        if step == 'goals':
            selected_goals = request.POST.getlist('goals')
            request.session['selected_goals'] = selected_goals
            return redirect('onboarding')  # This will now redirect to the 'profile' step
        
        elif step == 'profile':
            gender = request.POST.get('gender')
            skin_types = request.POST.getlist('skin_types')
            skin_conditions = request.POST.getlist('skin_conditions')
            
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.gender = gender
            profile.skin_types.set(SkinType.objects.filter(id__in=skin_types))
            profile.skin_conditions.set(SkinCondition.objects.filter(id__in=skin_conditions))
            profile.skincare_goals.set(SkincareGoal.objects.filter(id__in=request.session.get('selected_goals', [])))
            profile.save()
            
            messages.success(request, 'Profile created successfully!')
            return redirect('profile')
    
    else:
        # Check if goals have been selected
        if 'selected_goals' in request.session:
            step = 'profile'
        else:
            step = 'goals'
    
    context = {
        'step': step,
        'skincare_goals': SkincareGoal.objects.all(),
        'skin_types': SkinType.objects.all(),
        'skin_conditions': SkinCondition.objects.all(),
    }
    return render(request, 'onboarding.html', context)

def pricing(request):
    subscription_tiers = SubscriptionTier.objects.all()
    
    # Get user's current subscription if any
    current_subscription = None
    if hasattr(request.user, 'profile'):
        current_subscription = request.user.profile.subscription_tier

    context = {
        'subscription_tiers': subscription_tiers,
        'current_subscription': current_subscription
    }
    return render(request, 'pricing.html', context)

@login_required
@subscription_required()
def daily_checkin(request):
    # Check if user has already checked in today
    today = timezone.now().date()
    existing_checkin = DailyCheckIn.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        form = DailyCheckInForm(request.POST, instance=existing_checkin)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.user = request.user
            checkin.save()
            messages.success(request, 'Daily check-in recorded successfully!')
            return redirect('profile')
    else:
        form = DailyCheckInForm(instance=existing_checkin)
    
    return render(request, 'checkin.html', {'form': form})
