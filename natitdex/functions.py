from this import d
import requests
from collections import namedtuple
from natitdex.classes import pokemon
import json
from cachetools import cached, TTLCache

ONE_DAY = 60 * 60 * 24


def get_pkmnid_and_pkmnname_from_string(pkmn_list, pkmn_name, langid):
    for row in pkmn_list.index:
        entry = pkmn_list["name"][row]
        if (entry.casefold() == pkmn_name.casefold()):
            pkmn_id = pkmn_list["pokemon_species_id"][row]
            allpokemon = pkmn_list.loc[pkmn_list.pokemon_species_id == pkmn_id, :].copy(
            )
            localized_pkmn = (allpokemon.loc[allpokemon.local_language_id == langid, [
                "pokemon_species_id", "name", ]])
            return localized_pkmn


def get_from_pokeapi(endpoint, value):
    try:
        # print(value)
        pokeapipkmn = requests.get(
            f"https://pokeapi.co/api/v2/{endpoint}/{value}")
        # print(pokeapipkmn)
        pokeapipkmn.raise_for_status()
    except requests.exceptions.RequestException as err:
        return "error"
    except requests.exceptions.HTTPError as errh:
        return "error"
    except requests.exceptions.ConnectionError as errc:
        return "error"
    except requests.exceptions.Timeout as errt:
        return "error"
    return pokeapipkmn.json()


def get_pkmn_from_pokeapi(pkmn, lang_id, pkmn_local_name, pkmn_list, lang_name):
    api_return = get_from_pokeapi("pokemon", pkmn)
    # jsondata = json.loads(data)
    if (api_return == "error"):
        return "error"
    # print(data)
    if (pkmn.isnumeric() == True):
        pkmn_localize = get_pkmnid_and_pkmnname_from_string(
            pkmn_list, api_return['name'], lang_id)
        pkmn_local_name = pkmn_localize['name'].to_string(index=False)
        api_return['name'] = pkmn_local_name
        # pkmn_types = []
    else:
        api_return['name'] = pkmn_local_name
    lang_types = []
    for type in api_return['types']:
        lang_types.append(get_type_lang_from_pokeapi(
            type['type']['name'], lang_name))
    api_return['types'] = ' | '.join(lang_types)

    lang_abilities = []
    for ability in api_return['abilities']:
        lang_abilities.append(get_ability_lang_from_pokeapi(
            ability['ability']['name'], lang_name))
    api_return['abilities'] = ' | '.join(lang_abilities)

    lang_stats = []

    for stat in api_return['stats']:
        temp_stat_lang = get_stats_lang_from_pokeapi(
            stat['stat']['name'], lang_name)
        return_stat = f"{temp_stat_lang}: " + str(stat["base_stat"])
        lang_stats.append(return_stat)

    api_return['stats'] = ' | '.join(lang_stats)

    pkmn_class = pokemon(
        api_return['id'],
        api_return['name'],
        api_return['types'],
        api_return['abilities'],
        api_return['species']['name'],
        api_return['stats'])
    return pkmn_class


def get_type_lang_from_pokeapi(type, langname):
    type_langs = get_from_pokeapi("type", type)
    for name in type_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)


def get_ability_lang_from_pokeapi(ability, langname):
    ability_langs = get_from_pokeapi("ability", ability)
    for name in ability_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)


def get_stats_lang_from_pokeapi(stat, langname):
    stat_langs = get_from_pokeapi("stat", stat)
    for name in stat_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)


def get_lang_name_from_id(id):
    lang_name = get_from_pokeapi("language", id)
    if (lang_name == "error"):
        return "error"
    # print(lang_name['name'])
    return lang_name['name']
