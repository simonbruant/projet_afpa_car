# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'afpa_car_2',
#         # 'NAME': 'afpa_car_new',
#         'USER': 'afpa_car',
#         'PASSWORD': '',
#         'HOST': '10.111.62.19',
#         'PORT': '',
#     }

# }
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}