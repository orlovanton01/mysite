from django.test import TestCase, Client

# Create your tests here.
from .models import Course
class CourseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Course.objects.create(
            owner = "skillbox",
            course_name = "Тестовый курс для юниттестов",
            price = 999,
            final_rating = 0,
            link = "https://kurshub.ru/go/?id=52865",
            training_period = 12
        )

    def test_course_name_label(self):
        course=Course.objects.get(course_name="Тестовый курс для юниттестов")
        field_label = course._meta.get_field('course_name').verbose_name
        # print(field_label)
        self.assertEquals(field_label,'course name')

    def test_get_owner_img_url(self):
        course=Course.objects.get(course_name="Тестовый курс для юниттестов")
        self.assertEquals(course.get_course_img_url(),"/media/skillbox.png")
        
    # def test_course_name(self):
    #     course=Course.objects.get(course_name="Тестовый курс для юниттестов")
    #     field = course.course_name
    #     # print(field_label)
    #     self.assertEquals(field,'Тестовый курс для тестов')    

    def test_training_period(self):
        course=Course.objects.get(course_name="Тестовый курс для юниттестов")
        field = course.training_period
        self.assertEquals(field, 12)

    # def test_first_name_max_length(self):
    #     course=Course.objects.get(id=1)
    #     max_length = course._meta.get_field('first_name').max_length
    #     self.assertEquals(max_length,100)

    # def test_object_name_is_last_name_comma_first_name(self):
    #     course=Course.objects.get(id=1)
    #     expected_object_name = '%s, %s' % (course.last_name, course.first_name)
    #     self.assertEquals(expected_object_name,str(course))


from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.http import JsonResponse
from mysite import loginhandler as lh

class RequestTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='TestUser', password='top_secret')
        
    
    def test_guest_session(self):
        # Create an instance of a GET request.
        request = self.factory.get('/session/')
        request.user = AnonymousUser()
        response = lh.session_view(request)

        json = JsonResponse({'isAuthenticated': False})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))

    def test_user_session(self):
        # Create an instance of a GET request.
        request = self.factory.get('/session/')
        request.user = self.user
        response = lh.session_view(request)

        json = JsonResponse({'isAuthenticated': True})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))
    
    def test_guest_whoami(self):
        # Create an instance of a GET request.
        request = self.factory.get('/whoami/')
        request.user = AnonymousUser()
        response = lh.whoami_view(request)

        json = JsonResponse({'isAuthenticated': False})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))

    def test_user_whoami(self):
        # Create an instance of a GET request.
        request = self.factory.get('/whoami/')
        request.user = self.user
        response = lh.whoami_view(request)

        json = JsonResponse({'username': 'TestUser', 'id' : 1})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))

    def test_guest_logout(self):
        response = self.client.get('/logout/')

        self.assertEquals(response.status_code, 400)

    def test_user_logout(self):
        self.client.login(username='TestUser', password='top_secret')
        response = self.client.get('/logout/')

        self.assertEquals(response.status_code, 200)

    def test_guest_login(self):
        response = self.client.post(path = '/loginuser/', data = {
            "username":'TestUser', 'password':'top_secret'
        },content_type="application/json")
        
        self.assertEquals(response.status_code, 200)
        
        json = JsonResponse({'detail': 'Successfully logged in.'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))
        

    def test_user_login(self):
        self.client.login(username='TestUser', password='top_secret')
        response = self.client.post('/loginuser/', {
            "username":'TestUser', 'password':'top_secret'
        })
        self.assertEquals(response.status_code, 400)

    def test_empty_username_login(self):
        response = self.client.post(path = '/loginuser/', data = {
            "username":None, 'password':'top_secret'
        },content_type="application/json")
        
        self.assertEquals(response.status_code, 400)
        
        json = JsonResponse({'detail': 'Please provide username and password.'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))

    def test_empty_password_login(self):
        response = self.client.post(path = '/loginuser/', data = {
            "username":'TestUser', 'password':None
        },content_type="application/json")
        
        self.assertEquals(response.status_code, 400)
        
        json = JsonResponse({'detail': 'Please provide username and password.'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))

    def test_credentials_login(self):
        response = self.client.post(path = '/loginuser/', data = {
            "username":'TestUser', 'password':'wrong_secret'
        },content_type="application/json")
        
        self.assertEquals(response.status_code, 400)
        
        json = JsonResponse({'detail': 'Invalid credentials.'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), str(json.content, encoding='utf8'))


class VueTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='TestUser', password='top_secret')
        
        self.client = Client()

