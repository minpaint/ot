// Утилиты для работы с датами
const dateUtils = {
    formatDate(date) {
        return new Intl.DateTimeFormat('ru-RU').format(date);
    },

    formatDateTime(date) {
        return new Intl.DateTimeFormat('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    },

    parseDate(dateString) {
        const parts = dateString.split('.');
        return new Date(parts[2], parts[1] - 1, parts[0]);
    }
};

// Утилиты для валидации
const validationUtils = {
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    isValidPhone(phone) {
        return /^\+?[\d\s-()]+$/.test(phone);
    },

    isValidName(name) {
        return /^[А-ЯЁа-яё\s-]+$/.test(name);
    }
};

// Утилиты для работы с формами
const formUtils = {
    serializeForm(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    },

    populateForm(form, data) {
        Object.entries(data).forEach(([key, value]) => {
            const field = form.elements[key];
            if (field) {
                field.value = value;
            }
        });
    },

    resetForm(form) {
        form.reset();
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.invalid').forEach(el => {
            el.classList.remove('invalid');
        });
    }
};

// Утилиты для работы с API
const apiUtils = {
    async fetchData(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }
};

// Экспорт утилит
window.utils = {
    date: dateUtils,
    validation: validationUtils,
    form: formUtils,
    api: apiUtils
};