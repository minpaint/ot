# ���������� �����������

������� ���������� ������������� ����������� � ������������� ����������.

## ���������

1. ����������� �����������
2. ������� ����������� ���������: `python -m venv venv`
3. ������������ ���������: `source venv/bin/activate` (Linux) ��� `venv\Scripts\activate` (Windows)
4. ���������� �����������: `pip install -r requirements/development.txt`
5. ������� ���� .env � ��������� ���������� ���������
6. ��������� ��������: `python manage.py migrate`
7. ������� �����������������: `python manage.py createsuperuser`
8. ��������� ������: `python manage.py runserver`

## ��������� �������

- `apps/` - ���������� �������
- `config/` - ��������� �������
- `templates/` - �������
- `static/` - ����������� �����
- `media/` - ����������� �����
- `requirements/` - ����������� �������