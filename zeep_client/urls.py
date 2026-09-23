from django.urls import path

from zeep_client.views import send_edovendor_test, send_edovendor, send_agrcard_test, send_agrcard, \
    send_envelope_via_proxy

urlpatterns = [
    path("send_agrcard_test/", send_agrcard_test, name="send_agrcard_test"),
    path("send_agrcard/", send_agrcard, name="send_agrcard"),
    path("send_envelope_via_proxy/", send_envelope_via_proxy, name="send_envelope_via_proxy"),
    path("send_edovendor_test/", send_edovendor_test, name="send_edovendor_test"),
    path("send_edovendor/", send_edovendor, name="send_edovendor")
]
