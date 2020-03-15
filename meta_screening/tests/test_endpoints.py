# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
# from django.urls import reverse
# from django_webtest import WebTest
# from model_bakery import baker
# from webtest.app import AppError
# from django.test.utils import override_settings, tag
# from edc_auth import EVERYONE
#
# User = get_user_model()
#
#
# def login(testcase, user=None, superuser=None, groups=None):
#     user = testcase.user if user is None else user
#     superuser = True if superuser is None else superuser
#     if not superuser:
#         user.is_superuser = False
#         user.is_active = True
#         user.save()
#         for group_name in groups:
#             group = Group.objects.get(name=group_name)
#             user.groups.add(group)
#     form = testcase.app.get(
#         reverse(settings.LOGIN_REDIRECT_URL)).maybe_follow().form
#     form["username"] = user.username
#     form["password"] = "pass"
#     return form.submit()
#
#
# @override_settings(SIMPLE_HISTORY_PERMISSIONS_ENABLED=True)
# class MetaEndpointTest(WebTest):
#     def setUp(self):
#         self.user = User.objects.create_superuser(
#             "user_login", "u@example.com", "pass")
#
#     def login(self, **kwargs):
#         return login(self, **kwargs)
#
#     @tag("webtest")
#     def test_home_everyone(self):
#         self.login(superuser=False, groups=[EVERYONE])
