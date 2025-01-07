from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Ad
from .forms import AdForm

class MyAdsView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)

class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, 'Your ad has been created!')
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    
    return render(request, 'ads/create_ad.html', {'form': form})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your ad has been updated!')
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    
    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Your ad has been deleted!')
        return redirect('ads:my_ads')
    
    return render(request, 'ads/delete_ad.html', {'ad': ad})

def sponsored_ads(request):
    ads = Ad.objects.filter(is_sponsored=True)
    return render(request, 'ads/sponsored_ads.html', {'ads': ads})
