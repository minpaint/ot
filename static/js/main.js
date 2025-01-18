// Функция для обновления списка подразделений
function updateDepartments() {
    const organizationSelect = document.getElementById('id_organization');
    const departmentSelect = document.getElementById('id_department');

    if (organizationSelect && departmentSelect) {
        organizationSelect.addEventListener('change', function() {
            const organizationId = this.value;

            if (organizationId) {
                fetch(`/employees/ajax/departments/?organization=${organizationId}`)
                    .then(response => response.json())
                    .then(data => {
                        departmentSelect.innerHTML = '<option value="">---------</option>';
                        data.departments.forEach(dept => {
                            departmentSelect.innerHTML += `
                                <option value="${dept.id}">${dept.name}</option>
                            `;
                        });
                        departmentSelect.disabled = false;
                    });
            } else {
                departmentSelect.innerHTML = '<option value="">---------</option>';
                departmentSelect.disabled = true;
            }
        });
    }
}

// Функция для обновления списка должностей
function updatePositions() {
    const departmentSelect = document.getElementById('id_department');
    const positionSelect = document.getElementById('id_position');

    if (departmentSelect && positionSelect) {
        departmentSelect.addEventListener('change', function() {
            const departmentId = this.value;

            if (departmentId) {
                fetch(`/employees/ajax/positions/?department=${departmentId}`)
                    .then(response => response.json())
                    .then(data => {
                        positionSelect.innerHTML = '<option value="">---------</option>';
                        data.positions.forEach(pos => {
                            positionSelect.innerHTML += `
                                <option value="${pos.id}">${pos.name}</option>
                            `;
                        });
                        positionSelect.disabled = false;
                    });
            } else {
                positionSelect.innerHTML = '<option value="">---------</option>';
                positionSelect.disabled = true;
            }
        });
    }
}

// Функция для предварительного просмотра изображения
function setupImagePreview() {
    const imageInput = document.getElementById('id_photo');
    const imagePreview = document.getElementById('photo-preview');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}

// Функция для отслеживания прогресса импорта
function setupImportProgress() {
    const importForm = document.getElementById('import-form');
    const progressBar = document.getElementById('import-progress');
    const statusText = document.getElementById('import-status');
    const errorsList = document.getElementById('import-errors');

    if (importForm) {
        importForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch('/import/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.import_id) {
                    checkImportStatus(data.import_id);
                }
            });
        });
    }

    function checkImportStatus(importId) {
        fetch(`/import/status/${importId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'processing') {
                    const progress = (data.processed / data.total) * 100;
                    progressBar.style.width = `${progress}%`;
                    statusText.textContent = `Обработано ${data.processed} из ${data.total}`;

                    setTimeout(() => checkImportStatus(importId), 1000);
                } else if (data.status === 'completed') {
                    progressBar.style.width = '100%';
                    statusText.textContent = 'Импорт завершен';

                    if (data.errors.length > 0) {
                        errorsList.innerHTML = data.errors.map(error => 
                            `<li class="list-group-item text-danger">${error}</li>`
                        ).join('');
                    }
                } else if (data.status === 'failed') {
                    statusText.textContent = 'Ошибка импорта';
                    statusText.classList.add('text-danger');

                    if (data.errors.length > 0) {
                        errorsList.innerHTML = data.errors.map(error => 
                            `<li class="list-group-item text-danger">${error}</li>`
                        ).join('');
                    }
                }
            });
    }
}

// Функция для подтверждения удаления
function setupDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                e.preventDefault();
            }
        });
    });
}

// Функция для отметки об ознакомлении с документом
function setupDocumentFamiliarization() {
    const familiarizeButtons = document.querySelectorAll('.familiarize-btn');

    familiarizeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const documentId = this.dataset.documentId;

            fetch(`/documents/${documentId}/familiarize/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    this.textContent = 'Ознакомлен';
                    this.classList.remove('btn-primary');
                    this.classList.add('btn-success');
                    this.disabled = true;
                }
            });
        });
    });
}

// Вспомогательная функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация всех функций при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    updateDepartments();
    updatePositions();
    setupImagePreview();
    setupImportProgress();
    setupDeleteConfirmation();
    setupDocumentFamiliarization();
});