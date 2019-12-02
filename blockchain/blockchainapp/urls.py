from django.conf.urls import url
from blockchainapp import views
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [

    url(r'^$', views.login, name='login'),
    url(r'^get_username$', views.get_userdata, name='get_userdata'),
    url(r'^get_blockchain$', views.get_blockchain, name='get_blockchain'),
    url(r'^get_balance$', views.get_balance, name='get_balance'),
    url(r'^do_transaction$', views.do_transaction, name='do_transaction'),
    url(r'^mine_transaction$', views.mine_transaction, name='mine_transaction'),
    url(r'^display_transaction$', views.display_transaction, name='display_transaction')


]