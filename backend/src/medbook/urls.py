from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .views import SomeProtectedView, TestListView, SignupView, VerifyCodeView, CustomTokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="MedBook API",
      default_version='v1',
      description="API for MedBook application",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Получение JWT токена по username и password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Токены получены",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Неверные учетные данные",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('api/protected-endpoint/', SomeProtectedView.as_view()),
    path('api/medical-tests/', TestListView.as_view(), name='medical-tests-list'),
]