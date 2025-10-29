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
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

# Create your views here.

def index(request):
    not_include = '.DS_Store'
    if settings.DEBUG:
        one_cikan_dir = os.path.join(settings.BASE_DIR, 'static', 'img','one_cikan')
        marka_dir = os.path.join(settings.BASE_DIR, 'static', 'img','markalar')
        masa_ustu_dir = os.path.join(settings.BASE_DIR, 'static', 'img','masaustu')
        mutfak_dir = os.path.join(settings.BASE_DIR, 'static', 'img','sira_disi')
        oda_dir = os.path.join(settings.BASE_DIR, 'static', 'img','oda_sunum')
    else:
        one_cikan_dir = staticfiles_storage.path('img/one_cikan')
        marka_dir = staticfiles_storage.path('img/markalar')
        masa_ustu_dir = staticfiles_storage.path('img/masaustu')
        mutfak_dir = staticfiles_storage.path('img/sira_disi')
        oda_dir = staticfiles_storage.path('img/oda_sunum')
    if not os.path.isdir(one_cikan_dir):
        files = []
    else:
        files = [f for f in os.listdir(one_cikan_dir) if os.path.isfile(os.path.join(one_cikan_dir, f)) and f != not_include]
    
    if not os.path.isdir(marka_dir):
        marka_files = []
    else:
        marka_files = [f for f in os.listdir(marka_dir) if os.path.isfile(os.path.join(marka_dir, f))and f != not_include]
    
    if not os.path.isdir(masa_ustu_dir):
        masaustu_files = []
    else:
        masaustu_files = [f for f in os.listdir(masa_ustu_dir) if os.path.isfile(os.path.join(masa_ustu_dir, f)) and f != not_include]
    
    if not os.path.isdir(mutfak_dir):
        mutfak_files = []
    else:
        mutfak_files = [f for f in os.listdir(mutfak_dir) if os.path.isfile(os.path.join(mutfak_dir, f)) and f != not_include]
    
    if not os.path.isdir(oda_dir):
        oda_files = []
    else:
        oda_files = [f for f in os.listdir(oda_dir) if os.path.isfile(os.path.join(oda_dir, f)) and f != not_include]
    
    

    context = {
        'once_cikan_files': files,
        'markalar':marka_files,
        'masaustu':masaustu_files,
        'mutfak_files':mutfak_files,
        'oda_files':oda_files,
               }
    return render(request,'index.html',context=context)

def about(request):
    return render(request,'about.html')

def kvkk(request):
    return render(request,'kvkk.html')

def cerez(request):
    return render(request,'cerez.html')


def add_katalog(kat_name):
    return f'{kat_name}_katalog.png'

def catalog(request):
    
    if settings.DEBUG:
        catalog_dir = os.path.join(settings.BASE_DIR, 'static','katalog')
    else:
        catalog_dir = staticfiles_storage.path('katalog')
    if not os.path.isdir(catalog_dir):
        files = ['Ndustrio_2024_Katalog.pdf', 'Empero2024_Katalog.pdf']
    else:
        files = [f for f in os.listdir(catalog_dir) if os.path.isfile(os.path.join(catalog_dir, f))]
    
    cat_files = [
        {'url':'https://drive.google.com/file/d/1C1G57Q5BTALq5Ti-DK6ybcAStmTEo4mm/view','text':'Yıldız Bakırcılık','img':add_katalog('yildiz')},
        {'url':'https://guralporselen.com.tr/Content/assets/catalog/digibone-2023-small.pdf','text':'Güral Porselen - Horeca Digibone','img':add_katalog('gural')},
        {'url':'https://guralporselen.com.tr/Content/assets/catalog/horeca-white-2022.pdf','text':'Güral Porselen - Horeca White','img':add_katalog('gural_white')},
        {'url':'https://guralporselen.com.tr/Content/assets/catalog/horeca-bone-2022.pdf','text':'Güral Porselen Horeca','img':add_katalog('gural_porselen')},
        {'url':'https://www.lavametal.com.tr/uploads/catalog/Lava-Product-Catalogue.pdf?_gl=1*bgbgt8*_gcl_au*MTc1NzUzNjQ4MC4xNzYxNTc2NDU0','text':'Lava Metal','img':add_katalog('lava')},
        {'url':'https://simplebooklet.com/workpad/workpad_download/pdf/3q9HqIuOWi9R36ZgnXcWkd/0/link','text':'NUDE','img':add_katalog('nude')},
        {'url':'https://biradli.com.tr/wp-content/uploads/2025/02/BIRADLI-2025.pdf','text':'Biradlı','img':add_katalog('biradli')},
        {'url':'https://www.abmmutfak.com/katalog.pdf','text':'ABM Mutfak','img':add_katalog('abm')},
        {'url':'https://www.pirge.com/catalog/pirge.pdf?srsltid=AfmBOoptkuR39L22zlTQqIb_DKOsm02k7HRAH7BvaMk571FnADXqnzc5','text':'Pirge','img':add_katalog('pirge')},
        {'url':'https://leaf-vics.com/wp-content/uploads/catalogs/2024/victorinox_catalog_EN_2024.pdf','text':'Victorinox','img':add_katalog('victorinox')},
        {'url':'https://plante.biz/alkan2025.pdf','text':'Alkan','img':add_katalog('alkan')},
        {'url':'https://drive.google.com/file/d/1xJim6MD3trXbiTpgXbWKmyHjciPCpQkd/view','text':'Peugeout','img':add_katalog('peugeot')},
        {'url':'https://www.robot-coupe.com/robot-coupe-global/Page%20Documentation/Catalogues/TR/Robot-Coupe_2025_Katalog_Turkce_Interactive.pdf','text':'Robot Coupe','img':add_katalog('robot')},
        {'url':'https://cancan.com.tr/wp-content/uploads/2025/10/2025-CANCAN-KATALOG-MB-KUCULTULMUS.pdf','text':'Cancan','img':add_katalog('cancan')},
        {'url':'https://drive.google.com/file/d/1eZsoP_fKv-dmtQRscvpTXJoLdhRKpSrf/view?usp=drive_link', 'text':'Kapp','img':add_katalog('kapp')},
        {'url':'https://drive.google.com/file/d/1IBB60Nj9jG0mnuFY58f_daEIdmRfd1Bq/view?usp=drive_link', 'text':'Samixir','img':add_katalog('samixir')},
        {'url':'https://drive.google.com/file/d/1klbyKNOFfeaEc6y5qTjZR1l5urE8K7ZG/view?usp=drive_link', 'text':'Remta','img':add_katalog('remta')},
        {'url':'https://drive.google.com/file/d/15ZHFLW66irY4CD6ia_hhAyYwaerhIlq9/view?usp=drive_link', 'text':'Paşabahçe Retail','img':add_katalog('pasabahce')},
        {'url':'https://drive.google.com/file/d/1NfdrYYjnARrX0h2nE1xCpQVk0bdXg2bz/view?usp=drive_link', 'text':'Paşabahçe Hospitality','img':add_katalog('pasabahce')},
        {'url':'https://drive.google.com/file/d/1EimmPxplrJHFxGMph8mIE4eswFpESQ-v/view?usp=drive_link', 'text':'Narin','img':add_katalog('narin')},
        {'url':'https://drive.google.com/file/d/1Nrw9wrB3uG7ImEh5YUxUh8vIBsL2-PeA/view?usp=drive_link', 'text':'Mateka','img':add_katalog('mateka')},
        {'url':'https://drive.google.com/file/d/10-NYDnTlC3E2XKNwyi2Fl5Ehl1YebNky/view?usp=drive_link', 'text':'Lugga','img':add_katalog('lugga')},
        {'url':'https://drive.google.com/file/d/1HW5BjYohZ5ysh_cIWVC8AT9BK-f3ZIPT/view?usp=drive_link', 'text':'Jumbo','img':add_katalog('jumbo')},
        {'url':'https://drive.google.com/file/d/1wy5taZ39EBKa3vRWM2elUQutphVXhkTe/view?usp=drive_link', 'text':'Iceinox','img':add_katalog('iceinox')},
        {'url':'https://drive.google.com/file/d/1Y300jOnQlj2cw5M3ctX--oFjZ2hDbjhT/view?usp=drive_link', 'text':'Gastrotech','img':add_katalog('gtech')},
        {'url':'https://drive.google.com/file/d/1ubLvaPGmA519wtSuBPzKmuk0cHDdb6Yo/view?usp=drive_link','text':'Fantom','img':add_katalog('fantom')},
        {'url':'https://drive.google.com/file/d/19m0M9PQsSMb0mpTPI9QFSpqFhDk59NbK/view?usp=drive_link', 'text':'By Bone','img':add_katalog('bybone')},
        {'url':'https://drive.google.com/file/d/1CJ1nWxz2J69nnuUNqJgARkX_pOc2W2H5/view?usp=drive_link', 'text':'Bosfor','img':add_katalog('bosfor')},
        {'url':'https://drive.google.com/file/d/1k7fQMsHoEV3QJxyCBfoub4WXeeYgmuuS/view?usp=drive_link', 'text':'Atalay','img':add_katalog('atalay')},
        {'url':'https://drive.google.com/file/d/1aDz38ilkXxuo9cvJlN2WaO3OL9iYOwcZ/view?usp=drive_link', 'text':'Atalay - Yerli','img':add_katalog('atalay_yerli')},
        {'url':'https://drive.google.com/file/d/1Q8oM4t44i1TlwKLfXoYDtmh5XHypUVz8/view?usp=drive_link', 'text':'Senox','img':add_katalog('senox')},
        {'url':'https://drive.google.com/file/d/1Gp_mdHTNhnuhLNSvQBkhZr5XzZlcRP7c/view?usp=drive_link','text':'Epinox','img':add_katalog('epinox')}
        ]
    context = {'catalog_files': files,'cat_files':cat_files}
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
        
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['index', 'about', 'contact','catalog']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Blog.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at