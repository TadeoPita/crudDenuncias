from django.db import models

class Denuncia(models.Model):
    archivo = models.FileField(upload_to='archivos_denuncias/', null=True, blank=True)
    TIPOS_DELITO = [
        ('robo', 'Robo'),
        ('fraude', 'Fraude'),
        ('violencia', 'Violencia'),
        ('homicidio', 'Homicidio'),
        ('secuestro', 'Secuestro'),
        ('extorsion', 'Extorsión'),
        ('trafico_drogas', 'Tráfico de Drogas'),
        ('trata_personas', 'Trata de Personas'),
        ('lesiones', 'Lesiones'),
        ('estafa', 'Estafa'),
    ]
    
    BARRIOS = [
        ('Agronomía', 'Agronomía'),
        ('Almagro', 'Almagro'),
        ('Balvanera', 'Balvanera'),
        ('Barracas', 'Barracas'),
        ('Belgrano', 'Belgrano'),
        ('Caballito', 'Caballito'),
        ('Chacarita', 'Chacarita'),
        ('Colegiales', 'Colegiales'),
        ('Constitución', 'Constitución'),
        ('Flores', 'Flores'),
        ('Floresta', 'Floresta'),
        ('La Boca', 'La Boca'),
        ('La Paternal', 'La Paternal'),
        ('Liniers', 'Liniers'),
        ('Mataderos', 'Mataderos'),
        ('Monserrat', 'Monserrat'),
        ('Núñez', 'Núñez'),
        ('Palermo', 'Palermo'),
        ('Parque Avellaneda', 'Parque Avellaneda'),
        ('Parque Chacabuco', 'Parque Chacabuco'),
        ('Parque Patricios', 'Parque Patricios'),
        ('Puerto Madero', 'Puerto Madero'),
        ('Recoleta', 'Recoleta'),
        ('Retiro', 'Retiro'),
        ('Saavedra', 'Saavedra'),
        ('San Cristóbal', 'San Cristóbal'),
        ('San Nicolás', 'San Nicolás'),
        ('San Telmo', 'San Telmo'),
        ('Vélez Sársfield', 'Vélez Sársfield'),
        ('Villa Crespo', 'Villa Crespo'),
        ('Villa del Parque', 'Villa del Parque'),
        ('Villa Devoto', 'Villa Devoto'),
        ('Villa Lugano', 'Villa Lugano'),
        ('Villa Luro', 'Villa Luro'),
        ('Villa Pueyrredón', 'Villa Pueyrredón'),
        ('Villa Urquiza', 'Villa Urquiza'),
    ]

    ESTADOS_DENUNCIA = [
        ('presentada', 'Presentada'),
        ('confirmada', 'Confirmada'),
        ('sentencia_definitiva', 'Sentencia Definitiva'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    nombre_demandante = models.CharField(max_length=100)
    dni_demandante = models.CharField(max_length=15)
    estado = models.CharField(max_length=20, choices=ESTADOS_DENUNCIA, default='presentada')
    tipo_delito = models.CharField(max_length=20, choices=TIPOS_DELITO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    barrio = models.CharField(max_length=100, choices=BARRIOS)
    fecha = models.DateField(null=True)
    documento_adjunto = models.FileField(upload_to='documentos_adjuntos/')

    def __str__(self):
        return self.titulo
