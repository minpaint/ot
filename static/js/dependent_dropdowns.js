document.addEventListener('DOMContentLoaded', function() {
    const organizationSelect = document.getElementById('id_organization');
    const departmentSelect = document.getElementById('id_department');

    function resetSelect(select, defaultText = '---------') {
        select.innerHTML = `<option value="">${defaultText}</option>`;
        select.disabled = true;
    }

    if (organizationSelect) {
        console.log('Найден select организации');

        organizationSelect.addEventListener('change', function() {
            const organizationId = this.value;
            console.log('Выбрана организация:', organizationId);

            resetSelect(departmentSelect, 'Выберите подразделение');

            if (organizationId) {
                const url = `/departments/by_organization/?organization_id=${organizationId}`;
                console.log('Отправка запроса:', url);

                fetch(url)
                    .then(response => {
                        console.log('Получен ответ:', response.status);
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Получены данные:', data);

                        if (data.departments && data.departments.length > 0) {
                            departmentSelect.disabled = false;
                            data.departments.forEach(dept => {
                                const option = new Option(dept.name, dept.id);
                                departmentSelect.add(option);
                            });
                        } else {
                            console.log('Нет подразделений для этой организации');
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка при загрузке подразделений:', error);
                        resetSelect(departmentSelect, 'Ошибка загрузки');
                    });
            }
        });

        // Если уже выбрана организация при загрузке страницы
        if (organizationSelect.value) {
            organizationSelect.dispatchEvent(new Event('change'));
        }
    }
});
