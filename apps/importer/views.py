from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ImportSession
from .forms import ImportForm
from .serializers import ImportSessionSerializer
from .services import ImportService

@login_required
def import_data(request):
    """Страница импорта данных"""
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_session = ImportService.create_import_session(form.cleaned_data)
            ImportService.process_import(import_session.id)
            return JsonResponse({
                'status': 'success',
                'import_id': import_session.id
            })
    else:
        form = ImportForm()

    return render(request, 'importer/import.html', {'form': form})

@login_required
def import_status(request, import_id):
    """Получение статуса импорта"""
    import_session = ImportSession.objects.get(pk=import_id)
    return JsonResponse({
        'status': import_session.status,
        'processed': import_session.processed_rows,
        'total': import_session.total_rows,
        'errors': import_session.errors
    })

@login_required
def download_template(request):
    """Скачивание шаблона для импорта"""
    content_type = request.GET.get('type')
    if not content_type:
        return JsonResponse({'error': 'Не указан тип данных'}, status=400)

    content = ImportService.get_import_template(content_type)
    response = HttpResponse(
        content,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=template_{content_type}.xlsx'
    return response

# API Views
class ImportSessionViewSet(viewsets.ModelViewSet):
    queryset = ImportSession.objects.all()
    serializer_class = ImportSessionSerializer

    @action(detail=False, methods=['post'])
    def start_import(self, request):
        """Запуск импорта через API"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            import_session = serializer.save()
            ImportService.process_import(import_session.id)
            return Response(
                {'import_id': import_session.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Получение статуса импорта через API"""
        import_session = self.get_object()
        serializer = self.get_serializer(import_session)
        return Response(serializer.data)