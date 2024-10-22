import samino
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os
import glob
from time import sleep
import random
from tqdm import tqdm

print("Spam follow - By Tanji")
email = ""
password = ""

client = samino.Client()
client.login(email=email, password=password)

clients = client.get_my_communities(size=100)
for x, name in enumerate(clients.name, 1):
    print(f"{x}.{name}")
communityid = clients.comId[int(input("Comunidad: "))-1]
sub_client = samino.Local(comId=communityid)
method_choice=int(input("Selecciona el tipo de usuarios; 1 recientes /2 online: ")) 

def invite():
    while True:
        archivos_txt = glob.glob("*.txt")
        for archivo in archivos_txt:
            if archivo == "recent_amino.txt":
                os.remove(archivo)

        nombre = "recent"
        users = []
        for x in range(0, 10000, 100):  # Estableciendo un límite inferior más razonable
            suma = x + 100
            if method_choice == 1:
                user = sub_client.get_all_users(usersType="recent", start=x, size=suma).userId
            elif method_choice == 2:
                user = sub_client.get_all_users(usersType="online", start=x, size=suma).userId
            users.extend(user)
            if not user or x > 11000:
                print(f"Se han generado {len(users)} usuarios en total.")
                break
            elif len(user) == 100:
                print("Se han generado 100 IDs de usuario.")
                sleep(0.55)
        
        # Escribir todos los usuarios en el archivo
        with open(nombre + f"_amino.txt", "w") as archivo_salida:
            for elemento in users:
                archivo_salida.write(elemento + "\n")
        print(f"Se han generado en total {len(users)} usuarios.")

        lideres = sub_client.get_all_users(usersType="leaders", start=0, size=100).userId
        curadores = sub_client.get_all_users(usersType="curators", start=0, size=100).userId
        staff = [*curadores, *lideres]

        blocker_users = client.get_blocker_users(start=0, size=100)
        blocked_ids = {*blocker_users}

        with open("recent_amino.txt", "r") as archivo_entrada:
            lineas = archivo_entrada.readlines()

        with open("recent_amino.txt", "w") as archivo_salida:
            for linea in lineas:
                user_id = linea.strip()
                if user_id not in staff and user_id not in blocked_ids:
                    archivo_salida.write(linea)
        print("Staff y usuarios bloqueadores removidos.")

        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                with open("recent_amino.txt", "r") as archivo:
                    users = [line.strip() for line in archivo]

                progress_bar = tqdm(total=len(users), desc="Progreso de spam", unit="usuarios")

                for x in range(0, len(users), 20):
                    users_batch = users[x:x + 20]
                    sub_client.follow(users_batch)
                    sleep(random.uniform(1, 1.5))
                    progress_bar.update(len(users_batch))
                progress_bar.close()

                print("Spam en curso.")

                # Aquí vuelves a usar la lista recent_amino.txt en orden inverso
                users.reverse()

                progress_bar = tqdm(total=len(users), desc="Progreso de spam", unit="usuarios")

                for x in range(0, len(users), 20):
                    users_batch = users[x:x + 20]
                    sub_client.follow(users_batch)
                    sleep(random.uniform(1, 1.5))
                    progress_bar.update(len(users_batch))
                progress_bar.close()

                print("Spam en curso inverso.")

            except Exception as e:
                print(f"Error: {e}")

        archivos_txt = glob.glob("*.txt")
        for archivo in archivos_txt:
            if archivo == "recent_amino.txt":
                os.remove(archivo)

        print("Spam realizado.")

if _name_ == "_main_":
    invite()