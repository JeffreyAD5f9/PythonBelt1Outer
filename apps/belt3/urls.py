from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index),
url(r'^register$', views.Register),
url(r'^gotowishlist$', views.GoToWishlist),
url(r'^gotoItemCreate$', views.GoToItemCreate),
url(r'^login$', views.Login),
url(r'^logout$', views.Logout),
url(r'^itemCreate$', views.ItemCreate),
url(r'^addWishItem/(?P<itemAdd>\d+)$', views.addExistingItem),
url(r'^remove/(?P<itemRemove>\d+)$', views.Remove),
url(r'^view/(?P<item>\d+)$', views.viewItem)

]
