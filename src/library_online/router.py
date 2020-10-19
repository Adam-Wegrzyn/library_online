from library.views import LibraryApi
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='library', viewset=LibraryApi, basename='library')

# for url in router.urls:
#     print(url, '\n')
