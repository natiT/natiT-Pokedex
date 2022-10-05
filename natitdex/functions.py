from io import StringIO
from this import d
import requests
from collections import namedtuple
from natitdex.classes import pokemon
from cachetools import cached, TTLCache
import pandas

ONE_DAY = 60 * 60 * 24




@cached(cache= TTLCache(maxsize= 10, ttl = ONE_DAY))
def get_pkmnid_and_pkmnname_from_string(pkmn_list, pkmn_name, langid):
    dataframe = pandas.read_csv(StringIO(pkmn_list))
    array = []
    for row in dataframe.index:
        entry = dataframe["name"][row]
        if (entry.casefold() == pkmn_name.casefold()):
            pkmn_id = dataframe["pokemon_species_id"][row]
            allpokemon = dataframe.loc[dataframe.pokemon_species_id == pkmn_id, :].copy(
            )
            localized_pkmn = (allpokemon.loc[allpokemon.local_language_id == langid, [
                "pokemon_species_id", "name", ]])
            array.append(localized_pkmn['pokemon_species_id'].to_string(
                        index=False))
            array.append(localized_pkmn['name'].to_string(
                        index=False))
            return array
    return "none"

@cached(cache= TTLCache(maxsize= 5, ttl = ONE_DAY))
def get_from_pokeapi(endpoint, value):
    try:
        # print(value)
        #print("Zeile 35 : Lese von der pokeAPI!")
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

@cached(cache= TTLCache(maxsize= 100, ttl = ONE_DAY))
def get_pkmn_from_pokeapi(pkmn, lang_id, pkmn_local_name, pkmn_list, lang_name):
    api_return = get_from_pokeapi("pokemon", pkmn)
    #print("Zeile 55 : " + str(type(api_return)))
    tempclass = api_return
    # jsondata = json.loads(data)
    if (api_return == "error"):
        return "error"
    # print(data)
    if (pkmn.isnumeric() == True):
        pkmn_localize = get_pkmnid_and_pkmnname_from_string(
            pkmn_list, api_return['name'], lang_id)
        if not pkmn_localize:
            out = f"{pokemon} not exist in Database"
        else:
            pkmn_local_name = pkmn_localize[1]
        api_return['name'] = pkmn_local_name
    else:
        api_return['name'] = pkmn_local_name

    lang_types = []
    #print("Zeile 73 : " + str(api_return['types']))
    if not isinstance(api_return['types'],str):

        for ttype in api_return['types']:
            #print("Zeile 77 : " + str(type(ttype)))
            lang_types.append(get_type_lang_from_pokeapi(
            ttype['type']['name'] , lang_name))
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

@cached(cache= TTLCache(maxsize= 20, ttl = ONE_DAY))
def get_type_lang_from_pokeapi(type, langname):
    type_langs = get_from_pokeapi("type", type)
    for name in type_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)

@cached(cache= TTLCache(maxsize= 20, ttl = ONE_DAY))
def get_ability_lang_from_pokeapi(ability, langname):
    ability_langs = get_from_pokeapi("ability", ability)
    for name in ability_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)

@cached(cache= TTLCache(maxsize= 10, ttl = ONE_DAY))
def get_stats_lang_from_pokeapi(stat, langname):
    stat_langs = get_from_pokeapi("stat", stat)
    for name in stat_langs['names']:
        if name['language']['name'] == langname:
            temp = name['name']
            return (temp)

# @cached(cache= TTLCache(maxsize= 5, ttl = ONE_DAY))

@cached(cache= TTLCache(maxsize= 20, ttl = ONE_DAY))
def get_lang_name_from_id(id):
    lang_name = get_from_pokeapi("language", id)
    if (lang_name == "error"):
        return "error"
    return lang_name['name']
