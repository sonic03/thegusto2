from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import os
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
import re
import requests
from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def kvkk(request):
    return render(request,'kvkk.html')

def cerez(request):
    return render(request,'cerez.html')

def catalog(request):
    catalog_dir = staticfiles_storage.path('katalog')
    if not os.path.isdir(catalog_dir):
        files = ['Ndustrio_2024_Katalog.pdf', 'Empero2024_Katalog.pdf']
    else:
        #files = [f for f in os.listdir(catalog_dir) if os.path.isfile(os.path.join(catalog_dir, f))]
        files = ['Empero2024_Katalog.pdf']
    is_path = os.listdir(catalog_dir)
    context = {'catalog_files': files}
    context['is_path'] = is_path
    context['cat_path'] = catalog_dir
    return render(request,'catalog.html',context=context)

def contact(request):
    content = {}
    content['skey'] = settings.RECATCHA_SITE_KEY
    return render(request,'contact.html',context=content)


def validate_phone_number(phone):
    pattern = r'^(?:\+90|0)?5\d{9}$'
    return bool(re.match(pattern, phone))

@csrf_exempt
def send_form(request):
    if request.method=="POST":
        try:
            post_data = request.POST
            name = post_data.get('fname')
            phone = post_data.get('phone')
            mail = post_data.get('email')
            msg = post_data.get('msg')
            captcha = post_data.get('captcha')
            if not captcha:
                return JsonResponse({'success':False,'msg':'Robot alanını kontrol ediniz'})
            
            if not name:
                return JsonResponse({'success':False,'msg':'İsim alanı boş bırakılamaz'})
            
            if not phone:
                return JsonResponse({'success':False,'msg':'Telefon alanı boş bırakılamaz'})
            
            if not validate_phone_number(phone):
                
                return JsonResponse({'success':False,'msg':'Telefon formatı hatalı'})
            
            if not mail:
                return JsonResponse({'success':False,'msg':'E-posta alanı boş bırakılamaz'})
            
            if not msg:
                return JsonResponse({'success':False,'msg':'Mesaj alanı boş bırakılamaz'})
            
            if len(msg) < 5:
                return JsonResponse({'success':False,'msg':'Mesaj alanı en az 5 karater olmalıdır'})
            
            
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': captcha
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result.get('success'):
                subject = 'İletisim Formu'
                message = """
                    İletişim Formu Bilgileri
                    İsim Soyisim : {} ,
                    Telefon : {},
                    Eposta : {},
                    Mesaj : {}
                """.format(name,phone,mail,msg)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['mrkayacik@yahoo.com']
                send_mail( subject, message, email_from, recipient_list )
                return JsonResponse({'success':True,'msg':'İşlem başarılı. En kısa sürede dönüş yapılacaktır'})

            else:
                return JsonResponse({'success':False,'msg':'Lütfen reCAPTCHA doğrulamasını tamamlayın.'})  
            
        except Exception as e:
            print(f'Hata: {e}')
            return JsonResponse({'success':False,'msg':'Sistemsel bir hata oluştu'})
        
        
def custom_404(request, exception):
    context = {
        'message': 'Aradığınız sayfa bulunamadı!',
    }
    return render(request, '404.html', context, status=404)

def blogs(request):
    content = {}
    blogs = Blog.objects.filter(is_active=True).order_by('-id')
    content['blogs'] = blogs
    return render(request,'blogs.html',context=content)

def blog_detail(request,slug):
    context = {}
    blog = get_object_or_404(Blog,slug=slug)
    context['blog']=blog
    return render(request,'blog_detail.html',context=context)

@csrf_exempt
def send_main(request):
    if request.method == 'POST':
        try:
            post_data = request.POST
            email = post_data.get('email')
            if not email:
                return JsonResponse({'success':False,'msg':'E-posta alanı boş bırakılamaz'})
            
            if not Mails.objects.filter(mail_address = email).exists():
                Mails.objects.create(mail_address = email)
                return JsonResponse({'success':True,'msg':'İşleminiz Başarılı'})
            else:
                return JsonResponse({'success':False,'msg':'Epostanız Kayıtlıdır.'})

        except Exception as e:
            return JsonResponse({'success':False,'msg':'Sistemsel Hata'})