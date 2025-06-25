> **IMPORTANT:**  
> This document is a TEMPLATE. All project models must be documented following THIS EXACT pattern.
> See the `agents.md` file at the project root for complete guidelines on documentation, testing, workflow, and integration with AI/human agents.

# Django Models for PROJECT_NAME

This document details the main models used in the PROJECT_NAME project, presenting real code examples, standardized docstrings, and field tables.

---

## accounts.models

### CustomUser

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user for PROJECT_NAME, integrating Django and Firebase authentication.

    Additional fields:
        - firebase_uid: User UID in Firebase
        - permission_level: User permission level
        - is_active: Indicates if the user is active
    """
    PERMISSION_LEVELS = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
        ('registered', 'Registered'),
    )

    firebase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    permission_level = models.CharField(max_length=10, choices=PERMISSION_LEVELS, default='registered')
    is_active = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='user_permissions'  # Nome relacionado único
    )

    def save(self, *args, **kwargs):
        """
        Garante que o username será igual ao email, caso não definido.
        """
        if not self.username:
            self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_permission_level_display()})"
```

| Campo             | Tipo         | Obrigatório | Opções/Choices                  | Descrição                                  |
|-------------------|--------------|-------------|---------------------------------|---------------------------------------------|
| firebase_uid      | CharField    | Não         | -                               | UID do usuário no Firebase                  |
| permission_level  | CharField    | Sim         | admin, editor, viewer, registered| Nível de permissão do usuário               |
| is_active         | BooleanField | Não         | -                               | Indica se o usuário está ativo              |
| user_permissions  | ManyToMany   | Não         | -                               | Permissões adicionais                       |

---

### Setting

```python
class Setting(models.Model):
    """
    Configuração do sistema para o app accounts.
    """
    ref = models.CharField(max_length=50, unique=True, verbose_name='Referência')
    description = models.TextField(verbose_name='Descrição')
    val = models.TextField(null=True, blank=True, verbose_name='Valor')

    class Meta:
        verbose_name = 'Configuração Accounts'
        verbose_name_plural = 'Configurações Accounts'
        ordering = ['description']

    def __str__(self):
        return self.ref

    @classmethod
    def get_setting(cls, ref):
        """
        Retorna o valor de uma configuração pela referência.
        """
        try:
            x = cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            x = None
        if not x:
            return None
        return x.val
```

| Campo       | Tipo      | Obrigatório | Descrição                                |
|-------------|-----------|-------------|-------------------------------------------|
| ref         | CharField | Sim         | Referência única da configuração          |
| description | TextField | Sim         | Descrição da configuração                 |
| val         | TextField | Não         | Valor associado à configuração            |

---

## website.models

### SettingWebsite

```python
class SettingWebsite(models.Model):
    """
    Configuração do sistema para o app website.
    """
    ref = models.CharField(max_length=50, unique=True, verbose_name='Referência')
    description = models.TextField(verbose_name='Descrição')
    val = models.TextField(null=True, blank=True, verbose_name='Valor')

    class Meta:
        verbose_name = 'Configuração Website'
        verbose_name_plural = 'Configurações Website'
        ordering = ['description']

    def __str__(self):
        return self.ref

    @classmethod
    def get_setting(cls, ref):
        """
        Retorna o valor de uma configuração pela referência.
        """
        try:
            x = cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            x = None
        if not x:
            return None
        return x.val
```

| Campo       | Tipo      | Obrigatório | Descrição                                |
|-------------|-----------|-------------|-------------------------------------------|
| ref         | CharField | Sim         | Referência única da configuração          |
| description | TextField | Sim         | Descrição da configuração                 |
| val         | TextField | Não         | Valor associado à configuração            |

---

### Contact

```python
class Contact(models.Model):
    """
    Mensagens enviadas pelo formulário de contato do site.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    c = models.CharField(max_length=255, blank=True, null=True)
    s = models.CharField(max_length=255, blank=True, null=True)
    m = models.CharField(max_length=255, blank=True, null=True)
    is_send_mail = models.BooleanField(default=False)
    sales_trigger = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
```

| Campo        | Tipo         | Obrigatório | Descrição                                      |
|--------------|--------------|-------------|-------------------------------------------------|
| name         | CharField    | Sim         | Nome do remetente                              |
| phone        | CharField    | Sim         | Telefone do remetente                          |
| email        | EmailField   | Sim         | E-mail do remetente                            |
| subject      | CharField    | Sim         | Assunto da mensagem                            |
| message      | TextField    | Sim         | Conteúdo da mensagem                           |
| c            | CharField    | Não         | Campo auxiliar                                 |
| s            | CharField    | Não         | Campo auxiliar                                 |
| m            | CharField    | Não         | Campo auxiliar                                 |
| is_send_mail | BooleanField | Não         | Indica se foi enviado e-mail                   |
| sales_trigger| TextField    | Não         | Texto de trigger de vendas                     |
| created_at   | DateTimeField| Não         | Data/hora do envio                             |

---

### Anamnese

```python
class Anamnese(models.Model):
    """
    Ficha/anamnese preenchida por usuários do site Corradi.
    """
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    historia = models.TextField()
    dicionario = models.JSONField()
    data_hora = models.DateTimeField(auto_now_add=True)
    is_send_mail = models.BooleanField(default=False)
    sales_trigger = models.TextField(blank=True, null=True)
    utm_source = models.CharField(max_length=255, null=True)
    utm_medium = models.CharField(max_length=255, null=True)
    utm_campaign = models.CharField(max_length=255, null=True)

    @property
    def dicionario_dict(self):
        """
        Retorna o campo dicionario como um dicionário Python.
        """
        import json
        try:
            return json.loads(self.dicionario)
        except Exception:
            return {}

    def __str__(self):
        return f"{self.name} - {self.email}"
```

| Campo         | Tipo          | Obrigatório | Descrição                                             |
|---------------|---------------|-------------|--------------------------------------------------------|
| name          | CharField     | Sim         | Nome do usuário                                       |
| last_name     | CharField     | Não         | Sobrenome                                             |
| weight        | CharField     | Não         | Peso                                                  |
| height        | CharField     | Não         | Altura                                                |
| age           | CharField     | Não         | Idade                                                 |
| email         | EmailField    | Sim         | E-mail do usuário                                     |
| whatsapp      | CharField     | Sim         | WhatsApp                                              |
| historia      | TextField     | Sim         | Histórico/anamnese                                    |
| dicionario    | JSONField     | Sim         | Dados adicionais (json)                               |
| data_hora     | DateTimeField | Não         | Data/hora de criação                                  |
| is_send_mail  | BooleanField  | Não         | Indica se foi enviado e-mail                          |
| sales_trigger | TextField     | Não         | Texto de trigger de vendas                            |
| utm_source    | CharField     | Não         | Origem da campanha (UTM)                              |
| utm_medium    | CharField     | Não         | Meio da campanha (UTM)                                |
| utm_campaign  | CharField     | Não         | Campanha (UTM)                                        |

---

## Observações
- Consulte as classes diretamente nos arquivos models.py para detalhes completos e métodos auxiliares.
- Siga o padrão de docstrings e comentários conforme o arquivo `agents.md` na raiz do projeto.
