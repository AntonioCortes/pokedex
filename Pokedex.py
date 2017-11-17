import requests
from tkinter import *
from tkinter import ttk
import tkinter as tk
import base64
import json
from urllib.request import urlopen
from pathlib import Path
#from PIL import Image


def buscar_pokemon(text_field, ventana_principal):

    api_base = 'http://pokeapi.co/api/v2/'
    api_base_pkmn = 'pokemon/'
    num_pokemon = str(text_field.get())

    if num_pokemon != "":

        ruta_datos_str = 'datos/' + str(num_pokemon)
        ruta_datos_path = Path(ruta_datos_str)
        ruta_imagen_str = 'images/pokemons/' + str(num_pokemon)
        ruta_imagen_path = Path(ruta_imagen_str)
        tipo = ''
        json_tipo = ''

        if not (ruta_datos_path.is_file() & ruta_imagen_path.is_file()):
            solicitud = requests.get(api_base + api_base_pkmn + num_pokemon)
            json_pkmn = solicitud.json()

            lista_jsons_stats = json_pkmn['stats']
            nombre = json_pkmn['name']
            peso = json_pkmn['weight'] / 10
            print(nombre)

            datos = 'Nombre: ' + nombre + '\nPeso: ' + repr(peso) + ' Kg\n'

            cont = 1
            for type in json_pkmn['types']:

                url = type['type']['url']
                solicitud = requests.get(url)
                json_tipo = solicitud.json()

                for name in json_tipo['names']:
                    idioma = name['language']['name']

                    if idioma == 'es':
                        tipo = name['name']

                datos += 'tipo' + str(cont) + ': ' +  tipo + '\n'
                cont += 1

            for stat in lista_jsons_stats:
                nombre_stat = stat['stat']['name']
                base_stat = str(stat['base_stat'])
                esfuerzo = str(stat['effort'])

                # añadir '\nEsfuerzo: ' + esfuerzo + a la linea siguiente para ver esfuerzo

                datos += nombre_stat + ': ' + base_stat + '\n'

            archivo_datos = open(ruta_datos_str, 'w')
            archivo_datos.write(datos)
            archivo_datos.close()

            url_json_sprite = json_pkmn['forms'][0]['url']
            solicitud = requests.get(url_json_sprite)
            json_sprite = solicitud.json()
            url_sprite = json_sprite['sprites']['front_default']
            image_byt = urlopen(url_sprite).read()

            archivo_foto = open(ruta_imagen_str, 'wb')
            archivo_foto.write(image_byt)
            archivo_foto.close()


        archivo_datos = open(ruta_datos_str, 'r')
        datos = archivo_datos.read()
        archivo_datos.close()


        archivo_image_byt = open(ruta_imagen_str, 'rb')
        image_byt = archivo_image_byt.read()

        image_b64 = base64.encodebytes(image_byt)
        photo_pkmn = tk.PhotoImage(data=image_b64)

        label_sprite.configure(image = photo_pkmn)
        label_sprite.image = photo_pkmn

        label_datos.configure(text = datos, bg = 'light blue')

        archivo_image_byt.close()



ventana_principal=Tk()
ventana_principal.config(bg='light blue',height=576,width=370)
ventana_principal.resizable(width=False, height=False)
ventana_principal.title('Pokedex')

photo_pokeball= PhotoImage(file = "images/pokeball.png")
photo_pokedex=PhotoImage(file='images/pokedex1.png')

background=Label(bg='light blue')
background.place(x=0,y=0)
background.config(image=photo_pokedex)

label_sprite=Label(ventana_principal, image = photo_pokeball, bg = 'light blue')
label_sprite.place(x = 60, y = 220)

label_datos = Label(ventana_principal,bg='light blue',fg='grey')
label_datos.place(x = 210, y = 220)

text_field_1 = Entry(ventana_principal,textvariable = 'caca' ,width = 3, bg = 'light blue',fg='grey')
text_field_1.place(x = 175, y = 390)

button_go = Button(ventana_principal,text='GO!', command = lambda: buscar_pokemon(text_field_1, ventana_principal))
button_go.place(x = 348, y = 410)
button_go.config(height = 3, width = 2, bg = 'firebrick4', fg = 'black',relief=GROOVE)

ventana_principal.mainloop()
