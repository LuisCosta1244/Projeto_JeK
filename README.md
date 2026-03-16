# Projeto_JeK
Projeto Técnico - Entrevista Hard Skills JeKnowledge

1. Criar umo Ambiente Virtual
```bash
python -m venv venv
```

2. Ativar o Ambiente Virtual
No Windows Command Prompt :

```Bash
venv\Scripts\activate
```

3. Instalar as Dependências
Agora que estás dentro do ambiente virtual, vamos instalar o Django e o Django REST Framework (DRF):

```Bash
pip install django djangorestframework django-cors-headers
```

4. Guardar as Dependências (Crucial para a Entrega)

```Bash
pip freeze > requirements.txt
```

Instalar dependências:
```bash 
pip install -r requirements.txt
```

5. Para correr a API
Executar  
```bash 
python manage.py runserver
```