from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProdutoViewSet, PedidoViewSet, PagamentoViewSet

# O Router cria automaticamente os links para listas e detalhes
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pagamentos', PagamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]