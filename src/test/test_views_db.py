# """Test requests from views"""
# from django.test import RequestFactory, TestCase
# from django.contrib.auth.models import AnonymousUser
#
#
# # pylint: disable=all
#
#
# # Create your tests here.
# from src.core.views import get_statistics_year
#
#
# class TestRequests(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#
#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('get_statistics_year')
#
#         # Or you can simulate an anonymous user by setting request.user to
#         # an AnonymousUser instance.
#         request.user = AnonymousUser()
#
#         # Test my_view() as if it were deployed at /customer/details
#         response = get_statistics_year(request, requested_year=2010)
#         # Use this syntax for class-based views.
#
#         self.assertEqual(response.status_code, 200)
