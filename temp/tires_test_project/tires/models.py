from django.db import models
from django.core import validators as val
from tires.utils.functions import get_file_path
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Tire(models.Model):
    name = models.CharField(max_length=1000, validators=[val.MinLengthValidator(1)])
    width = models.PositiveSmallIntegerField(help_text='mm', validators=[val.MinValueValidator(1),
                                                                         val.MaxValueValidator(999)])
    height = models.PositiveSmallIntegerField(help_text='mm', validators=[val.MinValueValidator(1),
                                                                          val.MaxValueValidator(999)])
    diameter = models.PositiveSmallIntegerField(help_text='mm', validators=[val.MinValueValidator(1),
                                                                            val.MaxValueValidator(1999)])
    speed_index = models.CharField(max_length=5, validators=[val.MinLengthValidator(1)])
    picture = models.ImageField(upload_to=get_file_path, null=True, blank=True)

    def save(self):
        """On save() resize picture to fill 350x350."""
        im = Image.open(self.picture)
        output = BytesIO()
        im.thumbnail((350, 350))
        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.picture = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.picture.name.split('.')[0],
                                            'image/jpeg', sys.getsizeof(output), None)
        super(Tire, self).save()
