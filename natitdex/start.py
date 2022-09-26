# MODULES
import pandas
import uvicorn
from unicodedata import name
from cachetools import cached, TTLCache
# ---- cache maybe?


# FUNCTIONS
from natitdex.functions import get_pkmnid_and_pkmnname_from_string
from natitdex.functions import get_pkmn_from_pokeapi
from natitdex.functions import get_lang_name_from_id
# CLASSES
from natitdex.classes import pokemon
from natitdex.classes import api_output


# Variables
ONE_DAY = 60 * 60 * 24
PORT = 80

def main():
    world_name_list = "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv"
    csv_name_list = pandas.read_csv(world_name_list)

    lang_id = 6
    pkmn_list = csv_name_list[["pokemon_species_id", "local_language_id", "name"]]

    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/dex/{pokemon}")
    async def read_pokemon(pokemon):
        pokemon = pokemon.replace("!dex ",'')
        print(pokemon)
        language_name = get_lang_name_from_id(lang_id)
        if(language_name == 'none'):
            return f"{pokemon} not exist in Database"
        if (language_name == "error"):
            return "The Language ID in the Script was not correct. Error can only be resolved by the hoster"
        if (pokemon.isnumeric() == True):
            pkmn_lang_name = pokemon
            pkmn_id = pokemon
        else:
            pkmn_lang_name = get_pkmnid_and_pkmnname_from_string(pkmn_list, pokemon, lang_id)
            pkmn_id = pkmn_lang_name['pokemon_species_id'].to_string(index=False)
        # pkmn_name = pkmn_lang_name['name'].to_string(index=False)
        # print(pkmn_id)
        # return(pkmn_id + " " + pkmn_name)
        api_pkmn = get_pkmn_from_pokeapi(pkmn_id, lang_id, pkmn_lang_name, pkmn_list, language_name)
        out = f"Pokedex Eintrag für {api_pkmn.name} - Typ: {api_pkmn.types} - Fähigkeiten: {api_pkmn.abilities} - Basiswerte: {api_pkmn.stats}"

        # return api_pkmn
        # out = get_pkmn_from_pokeapi(pkmn_id)
        return out
    uvicorn.run(app, host="0.0.0.0", port=PORT)
