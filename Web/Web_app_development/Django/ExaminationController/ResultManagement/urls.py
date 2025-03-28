from rest_framework import routers
from ResultManagement.views import StudentViewSet, UniversityViewSet, ResultViewSet
router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'universities', UniversityViewSet)
router.register(r'result', ResultViewSet)
urlpatterns = router.urls
