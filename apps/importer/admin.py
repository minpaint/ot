from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import ImportSession
from .forms import ImportForm
from .services.import_handler import handle_import


@admin.register(ImportSession)
class ImportSessionAdmin(admin.ModelAdmin):
    """
    Админ-модель для управления импортом данных
    """
    list_display = (
        'content_type',
        'status',
        'processed_rows',
        'total_rows',
        'created',
        'updated'
    )

    list_filter = (
        'status',
        'content_type',
        'created'
    )

    readonly_fields = (
        'status',
        'errors',
        'processed_rows',
        'total_rows',
        'created',
        'updated'
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(self.import_view),
                name='data-import'
            ),
        ]
        return custom_urls + urls

    def import_view(self, request):
        if request.method == 'POST':
            form = ImportForm(request.POST, request.FILES)
            if form.is_valid():
                import_session = form.save()
                handle_import.delay(import_session.id)
                self.message_user(
                    request,
                    'Импорт данных начат. Результаты будут доступны в списке сессий.'
                )
                return self.response_post_save_change(request, None)
        else:
            form = ImportForm()

        context = {
            **self.admin_site.each_context(request),
            'title': 'Импорт данных',
            'form': form,
            'opts': self.model._meta,
        }

        return TemplateResponse(
            request,
            'admin/importer/import_form.html',
            context
        )