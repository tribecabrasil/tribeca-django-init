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
        related_name='user_permissions'  # Unique related name
    )

    def save(self, *args, **kwargs):
        """
        Ensure the username matches the email if not already defined.
        """
        if not self.username:
            self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_permission_level_display()})"
```

| Field            | Type         | Required | Options/Choices                    | Description                                 |
|------------------|--------------|----------|-----------------------------------|---------------------------------------------|
| firebase_uid     | CharField    | No       | -                                 | User UID in Firebase                        |
| permission_level | CharField    | Yes      | admin, editor, viewer, registered | User permission level                       |
| is_active        | BooleanField | No       | -                                 | Indicates whether the user is active        |
| user_permissions | ManyToMany   | No       | -                                 | Additional permissions                      |

---

### Setting

```python
class Setting(models.Model):
    """
    System configuration for the accounts app.
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
        Returns the value of a setting by reference.
        """
        try:
            x = cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            x = None
        if not x:
            return None
        return x.val
```

| Field       | Type      | Required | Description                           |
|-------------|-----------|----------|---------------------------------------|
| ref         | CharField | Yes      | Unique setting reference              |
| description | TextField | Yes      | Setting description                   |
| val         | TextField | No       | Value associated with the setting     |

---

## website.models

### SettingWebsite

```python
class SettingWebsite(models.Model):
    """
    System configuration for the website app.
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
        Returns the value of a setting by reference.
        """
        try:
            x = cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            x = None
        if not x:
            return None
        return x.val
```

| Field       | Type      | Required | Description                           |
|-------------|-----------|----------|---------------------------------------|
| ref         | CharField | Yes      | Unique setting reference              |
| description | TextField | Yes      | Setting description                   |
| val         | TextField | No       | Value associated with the setting     |

---

### Contact

```python
class Contact(models.Model):
    """
    Messages sent through the site's contact form.
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

| Field        | Type         | Required | Description                          |
|--------------|--------------|----------|--------------------------------------|
| name         | CharField    | Yes      | Sender name                          |
| phone        | CharField    | Yes      | Sender phone                         |
| email        | EmailField   | Yes      | Sender email                         |
| subject      | CharField    | Yes      | Message subject                      |
| message      | TextField    | Yes      | Message content                      |
| c            | CharField    | No       | Auxiliary field                      |
| s            | CharField    | No       | Auxiliary field                      |
| m            | CharField    | No       | Auxiliary field                      |
| is_send_mail | BooleanField | No       | Indicates if an email was sent       |
| sales_trigger| TextField    | No       | Sales trigger text                   |
| created_at   | DateTimeField| No       | Date/time sent                       |

---

### Anamnese

```python
class Anamnese(models.Model):
    """
    Anamnesis form completed by Corradi website users.
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
        Return the `dicionario` field as a Python dictionary.
        """
        import json
        try:
            return json.loads(self.dicionario)
        except Exception:
            return {}

    def __str__(self):
        return f"{self.name} - {self.email}"
```

| Field         | Type          | Required | Description                          |
|---------------|---------------|----------|--------------------------------------|
| name          | CharField     | Yes      | User name                            |
| last_name     | CharField     | No       | Last name                            |
| weight        | CharField     | No       | Weight                               |
| height        | CharField     | No       | Height                               |
| age           | CharField     | No       | Age                                  |
| email         | EmailField    | Yes      | User email                           |
| whatsapp      | CharField     | Yes      | WhatsApp                             |
| historia      | TextField     | Yes      | History/anamnesis                    |
| dicionario    | JSONField     | Yes      | Additional data (json)               |
| data_hora     | DateTimeField | No       | Creation date/time                   |
| is_send_mail  | BooleanField  | No       | Indicates if an email was sent       |
| sales_trigger | TextField     | No       | Sales trigger text                   |
| utm_source    | CharField     | No       | Campaign source (UTM)                |
| utm_medium    | CharField     | No       | Campaign medium (UTM)                |
| utm_campaign  | CharField     | No       | Campaign (UTM)                       |

---

## Notes
- Refer to the classes in the `models.py` files for full details and helper methods.
- Follow the docstring and comment style described in the `agents.md` file at the project root.
