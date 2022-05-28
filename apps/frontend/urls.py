
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from fornecedor.views import (
    import_csv, export_csv, 
    all_fornecedores, FornecedorEdit,
    FornecedorCreate,
    )
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('import/', import_csv, name='import_csv'),
    path('export/', export_csv, name='export_csv'),
    path('upload-file/', all_fornecedores, name='all_fornecedores'),

    path('editar-fornecedor/', FornecedorEdit.as_view(), name='FornecedorEdit'),
    path('criar-fornecedor/', FornecedorCreate, name='Create_Fornecedor')


]

# Para carregar STATIC e as MIDIAS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)