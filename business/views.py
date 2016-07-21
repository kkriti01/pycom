import requests

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View

from business.forms import FacebookPageSearchForm
from business.models import Business


class BusinessListView(View):

    def get(self, request, *args, **kwargs):
        businesses = Business.objects.all()
        return render(request, 'business_list.html', {'businesses': businesses})


class PopulateBusiness(View):

    def post(self, request, *args, **kwargs):
        form = FacebookPageSearchForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            url = 'https://graph.facebook.com/v2.7/search'
            params = {
                'q': form.cleaned_data['search_key'],
                'type': 'page',
                'fields': 'name,fan_count,phone,emails,street,location,city,zip,country,category',
                'access_token': form.cleaned_data['access_token']
            }
            r = requests.get(url, params=params)
            result = r.json()
            if 'error' in result:
                print(result)
                messages.error(request, 'Access Token is invalid, please check and retry.')
                return render(request, 'populate_business.html', {'form': form})
            else:
                for page in result['data']:
                    print(page['id'])
                    self.save_to_db(page)
                print(result.get('paging', {}))
                next_url = result.get('paging', {}).get('next', False)
                while next_url:
                    r = requests.get(next_url)
                    result = r.json()
                    for page in result['data']:
                        self.save_to_db(page)
            messages.success(request, 'Business successfully populated.')
            return redirect(reverse('home'))
        else:
            return render(request, 'populate_business.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = FacebookPageSearchForm()
        return render(request, 'populate_business.html', {'form': form})

    def save_to_db(self, page):
        if not page.get('name') and page.get('location', {}).get('street'):
            # page should have at least name and address
            return False
        business_data = {
            'page_id': page['id'],
            'name': page.get('name', ''),
            'email': page.get('email', ''),
            'phone': page.get('phone', ''),
            'street': page.get('location', {}).get('street', ''),
            'city': page.get('location', {}).get('city', ''),
            'pin': page.get('location', {}).get('zip', ''),
            'country': page.get('location', {}).get('country', ''),
            'likes': page.get('fan_count', 0),
            'category': page.get('category', '')
        }
        try:
            business, created = Business.objects.get_or_create(
                name=business_data['name'],
                page_id=business_data['page_id']
            )
            if created:
                business.__dict__.update(business_data)
                business.save()
                print('--{}: Saved'.format(page['id']))
                return True
            else:
                print('--{}: Business already exists'.format(page['id']))
                return False
        except Exception as e:
            print(e)
            return False
