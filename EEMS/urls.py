from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, LogoutView
from employees.views import EmployeeProfileViewSet
from employees.views import TerminateEmployeeView
from users.views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from attendance import views as attendance_views
from leaves import views as leave_views



router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'employees', EmployeeProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Router APIs
    path('api/', include(router.urls)),

    # Login

    path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Logout 👇
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/employees/terminate/<int:pk>/', TerminateEmployeeView.as_view()),

    # Attendance URLs
    path('check-in/', attendance_views.check_in, name='check_in'),
    path('check-out/', attendance_views.check_out, name='check_out'),   
    path('monthly-report/', attendance_views.monthly_report, name='monthly_report'),

    #leaves
    path('apply-leave/', leave_views.apply_leave),
    path('approve-leave/<int:leave_id>/', leave_views.approve_leave),
    path('leave-history/', leave_views.leave_history),
    path('all-leaves/', leave_views.all_leave_requests),
    path('my-leave-balance/', leave_views.my_leave_balance),
]