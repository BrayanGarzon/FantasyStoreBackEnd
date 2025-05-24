from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail





class Settings(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Configuración")
        verbose_name_plural = _("Configuraciones")


class Country(models.Model):
    """
    Represents countries.
    """
    name = models.CharField(_("Nombre de País"), max_length=255)
    iso_code = models.CharField(_("ISO Code"), max_length=3, unique=True)  # ISO 3166-1 alpha-3 code
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Paises")
        ordering = ("name",)

    def __str__(self):
        return self.name


class State(models.Model):
    """
    Departamentos de Colombia
    """
    country = models.ForeignKey(
        Country, related_name="states",
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Nombre del Departamento"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    geonames_code = models.CharField(_("Código GeoNames"), max_length=10, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    @classmethod
    def get_state_by_name(cls, name):
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            print(name)
            return None

    class Meta:
        verbose_name = _("Departamento")
        verbose_name_plural = _("Departamentos")
        ordering = ("name",)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Ciudades de Colombia
    """
    state = models.ForeignKey(
        State,
        related_name='cities',
        verbose_name=_("Municipios"),
        on_delete=models.CASCADE)
    name = models.CharField(_("Nombre del Municipio"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    slug = AutoSlugField(populate_from='name')
    coords_lat = models.FloatField(null=True, blank=True)
    coords_long = models.FloatField(null=True, blank=True)
    geo_location = models.PointField(null=True, blank=True)

    @classmethod
    def get_city_by_name(cls, name, state):
        try:
            if state:
                return cls.objects.get(name__iexact=name, state_id=state.id)
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            return None

    class Meta:
        verbose_name = _("Municipios")
        verbose_name_plural = _("Municipios")
        ordering = ("name",)

    def __str__(self):
        return '%s, %s' % (self.name, self.state.name)

    def save(self, *args, **kwargs):
        if self.coords_lat:
            point = Point(self.coords_long, self.coords_lat)
            self.location = point
        super(City, self).save(*args, **kwargs)


class Client(models.Model):
    name = models.CharField(_("Nombre del Cliente"), max_length=255)
    phone = models.CharField(_("Telefone"), max_length=255)

    def __str__(self):
        return self.name


class UnitOfMeasurement(models.Model):
    name = models.CharField(_("Nombre del UnitOfMeasurement"), max_length=255)

    def __str__(self):
        return self.name


class ImageTypeModel(models.Model):
    name = models.CharField(_("Nombre de la imagen"), max_length=255)

    class Meta:
        verbose_name = _("Tipo de Imagen")
        verbose_name_plural = _("Tipos de Imagenes")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(_("Image"), upload_to="images/")
    type = models.ForeignKey(ImageTypeModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.image.url.split('/')[-1]


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ColorModel(models.Model):
    name = models.CharField(_("Nombre de la color"), max_length=255)
    hex = models.CharField(_("Hex"), max_length=255)

    def __str__(self):
        return self.name

    ## TODO: validate format
    def save(self, *args, **kwargs):
        self.hex = self.hex.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colores")
        ordering = ("name",)


class SizeModel(models.Model):
    name = models.CharField(_("Nombre de la tamaño"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tamaño")
        verbose_name_plural = _("Tamaños")
        ordering = ("name",)


class ProductDistributionModel(models.Model):
    color = models.ForeignKey(ColorModel, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeModel, on_delete=models.CASCADE)
    stock = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    images = models.ManyToManyField(Image, related_name='product_distribution', blank=True)

    def __str__(self):
        return f"{self.color} - {self.size}"

    class Meta:
        verbose_name = _("Distribución de Producto")
        verbose_name_plural = _("Distribuciones de Productos")
        ordering = ("color", "size")


class CarouselItemModel(models.Model):
    title = models.CharField(_("Titulo"), max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.title} - {self.image.image.url.split('/')[-1]}"

    class Meta:
        verbose_name = _("Carousel Item")
        verbose_name_plural = _("Carousel Items")
        ordering = ("order",)


class ContactModel(models.Model):
    name = models.CharField(_("Nombre"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=255)
    phone = models.CharField(_("Telefono"), max_length=255, blank=True, null=True)
    created = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )

    class Meta:
        verbose_name = _("Contacto")
        verbose_name_plural = _("Contactos")
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.phone}'


    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        store_url = Settings.objects.filter(key='store_url').first().value if Settings.objects.filter(
            key='store_url').exists() else 'https://www.tutienda.com'

        try:
            if self.email:
                subject = _("Subcripcion Para Recivir Notificaciones")
                html_message = render_to_string("contact.html", {
                    'email': self.email,
                    'store_url': store_url,
                })
                send_mail(subject, '',  settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False,
                          html_message=html_message)
        except Exception as e:
            print(e)
        super().save(*args, **kwargs)