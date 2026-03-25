import googlemaps
import time

# Vlož svůj Google API klíč
gmaps = googlemaps.Client(key='AIzaSyA0p9PChtW3az6yiww2xa42-Hm9z4A_wwc')

def ziskej_restaurace(mesto):
    print(f"Hledám restaurace v: {mesto}")
    # Vyhledáme restaurace v daném městě
    places_result = gmaps.places(query=f'restaurants in {mesto}')
    
    weby = []
    for place in places_result.get('results', []):
        # Pro každou restauraci zjistíme detaily (včetně webu)
        details = gmaps.place(place_id=place['place_id'], fields=['name', 'website'])
        res = details.get('result', {})
        if 'website' in res:
            print(f"Nalezen web: {res['website']}")
            weby.append(res['website'])
    
    return weby

# Zkusíme třeba Prahu
seznam = ziskej_restaurace("Prague")
with open("weby_restauraci.txt", "w") as f:
    for web in seznam:
        f.write(web + "\n")

