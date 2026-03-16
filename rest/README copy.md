    
```bash
python -m venv venv
```

2. Ativar o Ambiente Virtual
Antes de instalares qualquer coisa, precisas de "entrar" nesse ambiente. O comando varia consoante o teu sistema operativo:

No Windows Command Prompt :

```Bash
venv\Scripts\activate
```

No macOS ou Linux:
```Bash
source venv/bin/activate
```

3. Instalar as Dependências
Agora que estás dentro do ambiente virtual, vamos instalar o Django e o Django REST Framework (DRF):

```Bash
pip install django djangorestframework django-cors-headers
```

4. Guardar as Dependências (Crucial para a Entrega)
Como o avaliador vai precisar de correr o teu código localmente, tens de lhe dizer que pacotes instalar. Podes gerar um ficheiro requirements.txt automaticamente com este comando:

```Bash
pip freeze > requirements.txt
```

No teu README.md, poderás depois dizer ao avaliador para simplesmente correr 
```bash 
pip install -r requirements.txt.
```