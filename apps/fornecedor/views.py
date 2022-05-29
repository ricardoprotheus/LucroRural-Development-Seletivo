from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
            ListView, UpdateView,
            DeleteView, CreateView,TemplateView
            )

from django.contrib import messages
from django.contrib.messages import constants

from .models import Fornecedor, Csv
from .forms import CsvForm, FornecedorForm
import csv


def export_csv(request):
    queryset = Fornecedor.objects.all()

    options = Fornecedor._meta
    fields = [field.name for field in options.fields]

    responde = HttpResponse(content_type='text/csv')
    responde['Content-Disposition'] = "atachment; filename:'fornecedor.csv'"

    write = csv.writer(responde)

    write.writerow([options.get_field(field).verbose_name for field in fields])

    for obj in queryset:
        write.writerow([getattr(obj, field) for field in fields])

    return responde

def import_csv(request):
    if request.method == 'POST':
        filename = request.get('import_file')#'csv/fornecedor.csv'
        print(filename)
        fornecedores = []
        with open(filename, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            for row in data[1:]:
                fornecedores.append(Fornecedor(
                    id=row['id'],
                    nome=row['nome'],
                    cnpj=row['cnpj'],
                    telefone=row['telefone']
                ))
        if len(fornecedores) > 0:
            Fornecedor.objects.bulk_create(fornecedores)
    else:
        print('Algo deu errado')

    return redirect('/')

def all_fornecedores(request):
    fornecedor = Fornecedor.objects.all().order_by('nome')
    form = CsvForm(request.POST, request.FILES or None)
    paginator = Paginator(fornecedor, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    if form.is_valid():
        form.save()
        form = CsvForm()
        obj = Csv.objects.get(activated=False)
        with open (obj.file_name.path, 'r') as f:
            reader = list(csv.reader(f, delimiter=";"))
            lista = []
            for rows in reader[1:]:
                lista.append(rows)
            for row in lista:
                import_fornecedores = Fornecedor.objects.update_or_create(
                    id=row[0],
                    nome=row[1],
                    cnpj=row[2],
                    telefone=row[3]
                )
            obj.activated = True
            obj.save()
            messages.add_message(request, constants.SUCCESS, 'Importação feita com sucesso')
            return redirect('/')
    context = {
        'fornecedor':fornecedor,
        'form':form,
        'posts':posts
    }
    return render(request, 'fornecedor/all_fornecedores.html',context)

def FornecedorCreate(request):
    form  = FornecedorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save() 
            messages.success(request, 'Novo fornecedor cadastrado com sucesso!')
            return redirect('all_fornecedores')
        else:
            messages.error(request, 'Novo fornecedor nao foi cadastrodo!')
            return redirect('Create_Fornecedor')

    return render(request, 'fornecedor/fornecedor_form.html',{'form':form})

class FornecedorEdit(UpdateView):
    template_name = 'fornecedor/FornecedorEdit.html'
    model: Fornecedor
    fields=['id', 'nome', 'cnpj', 'telefone']

class FornecedorDelete(DeleteView):
    model = Fornecedor
    success_url = reverse_lazy('all_fornecedores')

def FornecedorDelete2(request, id=None):
    fornecedor_remover = get_object_or_404(FornecedorForm, id=id)
    if request.method == "POST": 
        fornecedor_remover.delete()
        messages.add_message(request, constants.SUCCESS, "Ponto turistico deletado com sucesso") #cliente removido
        return redirect('index')
    return render(request, 'cadastro/deletar_ponto_turistico.html',{'fornecedor_remover':fornecedor_remover})
