# MODULES
import pandas
import uvicorn
from unicodedata import name
from cachetools import cached, TTLCache
from urllib.request import urlopen
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
world_name_list = "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species_names.csv"
#request_json = urlopen('https://natit.de/files/lang_list_minify.json')
#print(request_json.json())
#pkmn_list = json.loads(request_json.read())
csv_name_list = pandas.read_csv(world_name_list)
csv_string = csv_name_list.to_csv(index=False)
lang_id = 6
# pkmn_list = csv_name_list[[
#    "pokemon_species_id", "local_language_id", "name"]]


def main():

    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    app = FastAPI()

    @app.get("/dex/{pokemon}", response_class=PlainTextResponse)
    async def read_pokemon(pokemon):
        pokemon = pokemon.replace("!dex ", '')
        #print(pokemon)
        language_name = get_lang_name_from_id(lang_id)

        if (language_name == "error"):
            return "The Language ID in the Script was not correct. Error can only be resolved by the hoster"

        else:
            if (pokemon.isnumeric() == True):
                pkmn_lang_name = pokemon
                pkmn_id = pokemon
            else:
                temp_outlangpkmn = get_pkmnid_and_pkmnname_from_string(
                    csv_string, pokemon, lang_id)
                if not temp_outlangpkmn:
                    out = f"{pokemon} not exist in Database"
                else:
                    pkmn_id = temp_outlangpkmn[0]
                    pkmn_lang_name = temp_outlangpkmn[1]

            api_pkmn = get_pkmn_from_pokeapi(
                pkmn_id, lang_id, pkmn_lang_name, csv_string, language_name)
            out = f"Pokedex Eintrag für {api_pkmn.name} - Typ: {api_pkmn.types} - Fähigkeiten: {api_pkmn.abilities} - Basiswerte: {api_pkmn.stats}"
            return out
    uvicorn.run(app, host="0.0.0.0", port=PORT)
