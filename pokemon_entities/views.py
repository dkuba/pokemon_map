import os

import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pogomap.settings import BASE_DIR
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/" \
                    "6e/%21.png/revision/latest/fixed-aspect-ratio-down/" \
                    "width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # tooltip=name,  # disable tooltip because of folium encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.photo:
            pokemon_photo_url = \
                get_absolute_pokemon_photo_url(pokemon_entity.pokemon.photo.url)
            add_pokemon(folium_map, pokemon_entity.latitude,
                        pokemon_entity.longitude, pokemon_photo_url)

    pokemons_on_page = []

    pokemons = Pokemon.objects.all()

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
        })
        if pokemon.photo:
            pokemons_on_page[-1]['img_url'] = pokemon.photo.url

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemons = Pokemon.objects.all()

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    for pokemon_entity in pokemon_entities:
        if requested_pokemon.photo:
            pokemon_photo_url = \
                get_absolute_pokemon_photo_url(requested_pokemon.photo.url)
            add_pokemon(
                folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
                pokemon_photo_url)

    pokemon_next_evolution = Pokemon.objects.filter(previous_evolution=
                                                    requested_pokemon)
    if pokemon_next_evolution:
        requested_pokemon.next_evolution = pokemon_next_evolution[0]

    return render(request, "pokemon.html",
                  context={'map': folium_map._repr_html_(),
                           'pokemon': requested_pokemon})


def get_absolute_pokemon_photo_url(relative_photo_url):
    return BASE_DIR.replace('\\', '/') + relative_photo_url
