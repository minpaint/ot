// Обработчик импорта данных
const importHandler = {
    init() {
        this.form = document.getElementById('import-form');
        this.progressContainer = document.getElementById('progress-container');
        this.progressBar = document.getElementById('progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.errorContainer = document.getElementById('error-container');

        if (this.form) {
            this.setupEventListeners();
        }
    },

    setupEventListeners() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleImport();
        });
    },

    async handleImport() {
        const formData = new FormData(this.form);
        this.progressContainer.style.display = 'block';

        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const data = await response.json();
            if (data.status === 'success') {
                this.checkImportStatus(data.import_id);
            } else {
                this.showError('Ошибка при начале импорта');
            }
        } catch (error) {
            this.showError('Ошибка при отправке формы: ' + error);
        }
    },

    async checkImportStatus(importId) {
        try {
            const response = await fetch(`/import/status/${importId}/`);
            const data = await response.json();

            const progress = (data.processed_rows / data.total_rows) * 100;
            this.updateProgress(progress, data.processed_rows, data.total_rows);

            if (data.errors && Object.keys(data.errors).length > 0) {
                this.showErrors(data.errors);
            }

            if (data.status !== 'completed' && data.status !== 'failed') {
                setTimeout(() => this.checkImportStatus(importId), 1000);
            } else if (data.status === 'completed') {
                this.showSuccess('Импорт успешно завершен');
            }
        } catch (error) {
            this.showError('Ошибка при проверке статуса: ' + error);
        }
    },

    updateProgress(percentage, processed, total) {
        this.progressBar.style.width = `${percentage}%`;
        this.progressText.textContent = 
            `Обработано: ${processed} из ${total} записей`;
    },

    showError(message) {
        this.errorContainer.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                ${message}
            </div>
        `;
    },

    showErrors(errors) {
        this.errorContainer.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <h4 class="font-bold">Ошибки при импорте:</h4>
                <ul class="list-disc list-inside">
                    ${Object.entries(errors).map(([row, error]) => `
                        <li>Строка ${row}: ${error}</li>
                    `).join('')}
                </ul>
            </div>
        `;
    },

    showSuccess(message) {
        this.errorContainer.innerHTML = `
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                ${message}
            </div>
        `;
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    importHandler.init();
});