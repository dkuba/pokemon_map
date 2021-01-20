from django.db import models


class Pokemon(models.Model):
    """Покемон"""

    title_ru = models.TextField(verbose_name='название на русском')
    title_en = models.TextField(verbose_name='название на английском',
                                blank=True)
    title_jp = models.TextField(verbose_name='название на японском',
                                blank=True)
    description = models.TextField(verbose_name='описание')
    photo = models.ImageField(verbose_name='фотография',
                              upload_to='pokemons', null=True, blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                           null=True,
                                           verbose_name='эволюционировал из')

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    """Экземпляр покемона"""

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                related_name='entities',
                                verbose_name='покемон')
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='дата и время появления',
                                       null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name=
                                          'дата и время исчезновения',
                                          null=True, blank=True)
    level = models.IntegerField(default=1, verbose_name='уровень',
                                null=True, blank=True)
    health = models.IntegerField(default=1, verbose_name='здоровье',
                                 null=True, blank=True)
    strength = models.IntegerField(default=1, verbose_name='сила',
                                   null=True, blank=True)
    defence = models.IntegerField(default=1, verbose_name='защита',
                                  null=True, blank=True)
    stamina = models.IntegerField(default=1, verbose_name='выносливость',
                                  null=True, blank=True)



