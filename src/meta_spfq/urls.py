from django.urls.conf import path
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import RedirectView, TemplateView

app_name = "meta_spfq"

urlpatterns = [
    path(
        "spfq-for-withdrawal-topic-guide/",
        xframe_options_exempt(
            TemplateView.as_view(
                template_name="meta_spfq/spfq_for_withdrawal_topic_guide.html"
            )
        ),
        name="spfq_for_withdrawal_topic_guide",
    ),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
