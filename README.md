# Entrega Final- Paris A. Ramos de Cervantes


Este proyecto utiliza los siguientes elementos solicitados en CoderHouse para proyecto final del curso de Python: 


## Instalación

El proyecto se desarollo utilizando un entorno virtual con la siguiente paquetería instalada (se genero el archivo requirements para su implementación de ser necesario...)

```asgiref==3.7.2
asgiref==3.7.2
Django==5.0.2
pillow==10.2.0
sqlparse==0.4.4
tzdata==2024.1

```

Se debe de inicializar el servidor de Django con el siguiente comando:
```powershell
python manage.py runserver
```

Para el caso de ejemplo de este proyecto se ha generado el siguiente *superuser*, independientemente de que se puede crear un usuario normal en el proyecto:
```
superuser: Paritime
pass: coder12345
```

## Proyecto RiskAgr
El proyecto RiskAgr sde divide en 3 aplicaciones de Django implementando la arquitectura MVT:

1. App_Usuarios que sirve para administrar el registro, el acceso y los perfiles de los usuarios en el sistema.

2. App_BlogAgri, que implementa un concepto CRUD para publicaciones de un blog, en esta caso noticias del sector agroalimentario, vinculada a la aplicación de usuarios para que solo los autores de las publicaciones tengan la capacidad de borrar o editar las publicaciones que ellos mismos hicieron. Aún cuando un admin (superusuario), mediante el enlace disponible para el sistema de administración de django puede eliminar cualquier publicación. 

3. App_RiskCalc, que simula un sistema mediante el cual se puede asociar solicitantes de crédito, con proyectos y por ultimo consultar los proyectos asociados a cada solicitante. 

Entre las 3 aplicaciones, se prentende abarcar los conceptos solicitados para la entrega final del proyecto, con el comcepto de CRUD aplicado en la App_BlogAgri y la consulta de registros creados en App_RiskCalc.

## Configuraciones

Se deben de tener las siguientes configuraciones y consideraciones iniciales: 

1. Se crearon  carpetas *static_files* , *templates* y *media*, en la raíz del directorio del proyecto, con el objetivo  administrar de una mejor manera, los elementos que se comparten entre todas las apps, como lo son los estilos de css, el template base que sirve de padre para las demas plantillas html de las apps y una carpeta para almacenar las imagenes que se cargan mediante los formularios de las apps. 

2. Lo anterior requirio modificar el archivo de **settings** del proyecto en los siguientes apartados:

Para templates se agregó el directorio 'DIRS': [os.path.join(BASE_DIR, 'templates')], que permite reconocer las carpetas que se llamen del mismo modo dentro del proyecto.
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
```
Para static_files se incluyó STATICFILES_DIRS para poder identificar la carpeta de la raíz prioncipal, mediante la siguiente ruta: 

```
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]

```
Para la carpeta que se utiliza para el almacenamiento de imagenes o archivos, *"media"*, se configuro la raíz del directorio y su URL mediante la implementación de: 

```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```
## Base de datos
EL proyecto utiliza Sqlite3 que es la base de datos por defecto de Django. 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```



## a) App_Usuarios
1. La aplicación permite crear, autentificar y modificar usuarios (únicamente los atributos seleccionados)
2. Cuenta con 3 templates, 4 vistas y 2 formularios.
3. Los formularios son personalizados con base en herencias de los incorporados por defecto por Django, que se utilizan para crear usuarios y para cambiar información de los mismos (**UserCreationForm y UserChangeForm**)
```
```
**Inicio de Sesion**
![App Screenshot](https://github.com/paritime/RISK_FINANCE_AGR/blob/Test_Paris/readme%20img/Login.png?raw=true)
```
```
**Registro**
![App Screenshot](https://github.com/paritime/RISK_FINANCE_AGR/blob/Test_Paris/readme%20img/Login.png?raw=true)
```
```
**Perfil con opción de editar**
![App Screenshot](https://github.com/paritime/RISK_FINANCE_AGR/blob/Test_Paris/readme%20img/Actualizar%20Perfil.png?raw=true)

## Review
Con la siguiente aplicación se pueden crear usuarios genéricos, que pueden hacer uso de App_RiskCalc y App_BlogAgri.

Para la creación de usuarios con permisos de administración, se opto por colocar un link en la barra de navegación del template, que en caso de ser superusuario, pemrite acceder al administrador proporcionado por Django. 

Uno de los puntos que deben resaltar de esta App, es que no se definio ningún modelo, sin embargo se utilizó una adaptación de formularios para la creación de usuarios y para la adición de algunos atributos. 

Tanto *UserCreationForm* como *UserChangeForm*, son formularios que derivan del **Modelo User** y por lo tanto ese es el modelo utilizado en esta App.

La elección de crear personalizaciones de formularios, se debio a que buscaba experimentar con los diferentes métodos para mostrar en el template solo ciertos campos, pero aprovechar las validaciones que ya exisitian en los formularios padres. 

El uso de Clases Meta para definir el modelo al que hacen referencia los formularios personalizados y la definición de campos especificos para mostrarse, ayudan para su implementación en los templates.

También la posibilidad de sobreescribir algunos métodos como save(), permite asignar variables a los modelos sin tener que pasarlos al formulario y/o asignar campos del formulario a los valores definidos en el modelo. 

**Creación de Usuarios**

```
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "nombres", "apellidos", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nombres"]
        user.last_name = self.cleaned_data["apellidos"]
        if commit:
            user.save()
        return user
```

**Edicion de Usuarios**
```
class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    password1 = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(
        label="Confirmar contraseña", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("username", "nombres", "apellidos",
                  "email", 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserChangeForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nombres"]
        user.last_name = self.cleaned_data["apellidos"]
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 == password2:
            user.set_password(password1)

        if commit:
            user.save()
        return user
```

Se utilizaron 4 vistas **(registro, ingresar, logout y perfil)** en el proyecto que utilizaron las funciones incorporadas en Django para autentificar, ingresar y salir de la cuenta de usuario:

```
from django.contrib.auth import login, authenticate, logout as auth_logout
```
También se utilizó el decorador login_required para poder simplificar el mostrar o no la vista en caso de que los usuarios no se encontraran autentificados

```
from django.contrib.auth.decorators import login_required
```



## b) App_BlogAgri

1. El objetivo de esta apliación es implementar un Blog para temas de agricultura, que los usuarios puedan consultar y que les permita borrar o modificar sus propias publicaciones. 

2. En esta App se desarrollo el concepto de CRUD, para lo cual se diseño lo siguiente:

2.1 Un modelo Post para almacenar la información de las publicaciones.

2.2 El campo de autor de la publicación se encuentra relacionado de uno a muchos con los usuarios. Es decir un usuario puede tener muchas publicaciones, pero una publicación solo puede tener un autor. 
```
autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
```
2.3 Se creo un campo mediante *models.SlugField* que funciona para que una vez definido el titulo de la publicación, al modificar el metodo save(), se genere un valor que posteriormente nos sirva para identificar publicaciones en la url y que sirva para el posicionamiento SEO del Blog:
```
    def save(self, *args, **kwargs):
        if not self.slug:
            # Si no hay un slug definido, genera uno a partir del título
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
```
2.4 Se genero un archivo choices.py para poder administrar las tuplas que sirven para aquellos campos del modelo que utilzan valores predefinidos, para el caso especifico de la App_BlogAgri, se definieron si las publicaciones son publicas o privadas y los tipos de categorias del blog. 

**Definicion de choices**
![App Screenshot](https://github.com/paritime/RISK_FINANCE_AGR/blob/Test_Paris/readme%20img/Choices.png?raw=true)

Con relación a los formularios, se definio **PostForm** con 5 campos:
```
    class Meta:
        model = Post
        fields = ['titulo', 'contenido',
                  'tema_post', 'imagen', 'status_post',]
```
También se utilizaron validaciones personalizadas que definieran errores para campos individuales como: 

```
    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        if len(contenido) < 100:  # Establece el mínimo a 100 caracteres
            raise forms.ValidationError(
                "El contenido debe tener al menos 100 caracteres.")
```
Y también para condiciones de varios campos como: 
```
    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        status_post = cleaned_data.get('status_post')

        if status_post == 1 and imagen is None:
            self.add_error('imagen', forms.ValidationError(
                "Debes subir una imagen para poder publicar o seleccionar la opción de borrador.",
                code='missing_image'))
        return cleaned_data
```

En cuanto a las vistas se definieron:

1. **blog** para listar las publicaciones de todos los usuarios del blog y que sean publicas.
2. **posts_user** para listar las publicaciones unicamente que corresponden al usuario autentificado.
3. **post** para obtener el contexto que permita renderizar los elementos necesarios para el template de cada publicación.
4. **create_post** para crear nuevas publicaciones
5. **edit_post** para renderizar un formulario que permita editar una publicación.
6. **confirm_delete** para generar un render con la confirmación para borrar un objeto.
7. **delete_post** para realizar el borrado de una publicación.
```
```
El uso de URL con parámetros, vistas y formularios para permitir la edición de objetos específicos en los modelos, se utilza ampliamente en esta App, lo cual se ve reflejado en su uso en Templates. Para el caso de las listar publicaciones se utilizo como parámetro de selección de objeto **post.slug** para que el navegador mostrara el titulo de manera amigable en el navegador y para la edición se utilizo **post.id** .

```
        <div class="card-content">
            <h2>{{ post.titulo }}</h2>
            <h4>De: {{ post.autor }}</h4>           
            <p>{{ post.contenido|slice:":200" }}...</p>  
            <a href='{% url "post" post.slug %}' class="btn-read-more">Leer más</a>
            {% if user == post.autor %}
                <a href='{% url "edit_post" post.id %}' class="btn-edit">Editar</a>
                <a href='{% url "confirm_delete" post.id %}' class="btn-delete">Borrar</a>
            {% endif %}   
```
También es importante señalar que la vinculación de esta App con las validaciones de usuarios, afecta el comportamiento de alguinos templates, en donde dependiendo si el usuario ha realizado alguina publicación se muestran en un apartado especial y en caso de no haber publicado nada, aún puede ver las publicaciones de otros usuarios, pero no puede editarlas o borrarlas, siendo posible únicamente aplicar el borrado y editado si el mismo usuario que las creo, las desea modificar. 

![App Screenshot](https://github.com/paritime/RISK_FINANCE_AGR/blob/Test_Paris/readme%20img/blogfoto.png?raw=true)


## c) App_RiskCalc

1. La app simula de manera preliminar un simulador de riesgo, al que pueden acceder usuarios registrados, losd cuales deben de seguir los siguientes pasos:
1.1 Acceder a Registro de Solicitantes, para crear el primer soliciante de crédito. 
1.2 Acceder a Vinculación de Proyectos, mediante el cual podemmos asignar un proyecto al listado de solicitantes de crédito.
1.3 Acceder a Niveles de Riesgo y seleccionar un Solicitante registrado
1.4 Si el solicitante tiene proyectos asignados, se mostrara la información de los proyectos asociados como en el siguiente ejemplo:

```
Proyectos asociados
Estado: HID
Municipio: Pachuca
Cultivo: cebada
Rendimiento: 15.00 toneladas x hectárea
Hectáreas: 25.00 HA
Riesgo: Bajo
```
1.5 En caso de no tener proyectos vinculados, se mostrará que no cuenta con proyectos. 

1.6 Si se ingresa con el superusuario definido en el apartado de Instalación de este documento, se podrán visualizar todos los solicitantes registrados por los usuarios.

1.7 En caso contrario, únicamente el usuario podrá visualizar la información que el mismo registre. 

## Review

1. La app implementa 3 modelos mediante los cuales se busca relacionar personas que soliciten creditos para el sector agroalimentario, con los paquetes tecnologícos (especificaciones como tecnología aplicada, tipo de cultivo, número de hectáreas... ), así como la ubicación en donde se desarrollara el proyecto, para poder generar un escenario del Riesgo del otorgamiento del credito asociado.

2. EL presente ejemplo, es una simplificación para poder implementar conceptos de programación mediante el framework de Django, entre otros: 

* Herencia de HTML (templates).
* Diseño y migración de modelos usando el ORM de Django.
* Implementación de formularios.
* Personalización de formularios inmtegrados en Django.
* Autorización y validación de usuarios mediante la clase *UserCreationForm*.
* Decoradores básicos como *login_required*.
* Validaciones personalizadas con *cleaned data*.
* Implementaicón de la clase User para poder asignar privilegios básicos entre SuperUser y User.
* Condicionales y bucles con *jinja* para renderizar elementos desde las vistas en los templates.

3. Las funciones y clases, tanto en vistas, modelos y forms del proyecto cuentan con docstring.

4. Se genero adicionalmente a lo requerido el archivo choices.py que permite almacenar las tuplas que se pueden utilizar en el contexto de la creacion de los modelos, para campos específicos, tales como los Estados de un País (para este caso México).}



## Modelos

El proyecto RiskAgr se encuentra diseñada en el patrón de arquitectura *Modelo - Vista -Template* de Django y cuenta con los siguientes modelos:


1 *Persona* con las siguientes caractéristicas

```
Atributos:
1. nombre (str): El nombre de la persona.
2. apellido_paterno (str): El apellido paterno de la persona.
3. apellido_materno (str): El apellido materno de la persona.
4. edad (int): La edad de la persona.
5. genero (str): El género de la persona. Puede ser 'M' para masculino o 'F' para femenino.
6. rfc (str): El Registro Federal de Contribuyentes (RFC) de la persona que se utiliza en Mexico para identificación.
7. user (User): El usuario registrado que crea el registro de la persona.
```

2 *Paquete_Tec* con las siguientes caractéristicas

```
Atributos:
1. nombre_cultivo (str): El nombre del cultivo al que se aplica el paquete tecnológico.
2. tecnologia_aplicada (str): La tecnología aplicada para el cultivo.
3. rendimiento_promedio (Decimal): El rendimiento promedio que ha reportado el productor.
4. hectareas (Decimal): La cantidad de hectáreas en las que se aplica el paquete tecnológico.
5. riesgo (str): El nivel de riesgo asociado al paquete tecnológico.
6. persona (Persona): La persona que solicita un credito asociada con el paquete tecnológico.
```

3 *Ubicacion* con las siguientes caractéristicas

```
Atributos:
1. estado (str): El estado de México donde se ubica el paquete tecnológico.
2. municipio (str): El municipio donde se ubica el paquete tecnológico.
3. persona (Persona): La persona que solicita el credito asociada con la ubicación del paquete tecnológico.
4. paquete_tec (Paquete_Tec): El paquete tecnológico asociado con la ubicación.
```

* Los modelos cuentan con una relación de muchos a uno, de tal forma que una Persona (solicitante de crédito), puede tener muchas solicitudes, con diferentes características (paquiete tecnológico y ubicaciones)

* También al hacer uso de la clase proporcionada por Django UserCreationForm, relacionamos estos modelos con el usaurio que genera los registros. Para que un usuario solo pueda visualizar la información que el ha registrado. Con excpeción del supersuser que puede visualizar toda la información registrada en la base de datos. 
## Formularios

*Se han generado formularios para cada modelo y también se ha personalizado el formulario proporcionado por Django mediante la siguiente clase:
```
CustomUserCreationForm(UserCreationForm)
```
Lo anterior con el objetivo de poder probar la implementación de campos adicionales a los establecidos por defecto en Django. 

También se genero un formulario para poder utilizarlo como filtro en la consulta de registros de la plataforma

```
ConsultaPersonaForm(forms.Form)
```
## Vistas

* Las vistas han implementado diferentes mecanismos tanto para validación de usuarios, como es el caso del decorador *@login_required*, como la creación de variables desde la vista para posteriormente ser almacenadas en los modelos:

*Generamos valores condicionales para riesgo, variable no definida en el formulario y que se calcula en el Backend
```
            riesgo = ''
            if tecnologia_aplicada == 'RA' and rendimiento_promedio >= 5:
                riesgo = 'Bajo'
            elif tecnologia_aplicada == 'RG' and rendimiento_promedio < 5:
                riesgo = 'Moderado'
            elif tecnologia_aplicada == 'TEMP' and rendimiento_promedio < 5:
                riesgo = 'Alto'
            else:
                riesgo = 'Bajo'
            print(riesgo)
```
*Guardamos los datos del formulario de paquete tecnólogico
```
            new_paq = formpaq.save(commit=False)
            new_paq.riesgo = riesgo  # Asignamos el riesgo calculado
            new_paq.save()  # Guardamos el objeto en la base de datos
```


## HTML Template

Para el caso de los templates se implemento codigo como el que se muestra a continuación para poder mostrar en el apartado de consulta, los conjuntos de objetos resultado de las consultas realizadas mediante comandos como * ubicaciones = Ubicacion.objects.filter(persona=persona)*

```
    {% if ubicaciones %}
    <div class="card">
        <h2>Proyectos asociados</h2>
        <ul class="list-group list-group-flush">
            {% for ubicacion in ubicaciones %}
            <li class="list-group-item">
                <strong>Estado:</strong> {{ ubicacion.estado }} <br>
                <strong>Municipio:</strong> {{ ubicacion.municipio }} <br>
                <strong>Cultivo:</strong> {{ ubicacion.paquete_tec.nombre_cultivo }} <br>
                <strong>Rendimiento:</strong> {{ ubicacion.paquete_tec.rendimiento_promedio }} toneladas x hectárea <br>
                <strong>Hectáreas:</strong> {{ ubicacion.paquete_tec.hectareas }} HA <br>
                <strong>Riesgo:</strong> {{ ubicacion.paquete_tec.riesgo }} <br>
            </li>
            {% endfor %}
        </ul>
    </div>
```