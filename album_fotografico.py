from operator import itemgetter

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    try:
        with open(file_path, "r",encoding='utf=8') as infile:

            album= {} #dizionario in cui ogni chiave è l'anno e il valore è una lista
            # di dizionari, in cui ogni dizionario rappresenta una foto
            infile.readline()
            for line in infile:
                line= line.rstrip("\n")
                line= line.split(",")
                if int(line[4]) not in album: #controllo se l'anno non è nel dizionario e nel
                    #caso lo aggiungo
                    album[int(line[4])]= []
                foto={
                    "codice": line[0],
                    "titolo": line[1],
                    "autore": line[2],
                    "mese": line[3]
                }

                album[int(line[4])].append(foto)



            print(album)
            return album


    except FileNotFoundError:
        print("None")




def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    #apro il file in modalità scrittura
    try:
        with open(file_path, "a", encoding='utf=8') as infile:
            if anno not in album:
                album[anno]= [] # rendo l'anno una chiave
            foto_nuova= {
                "codice": codice,
                "titolo": titolo,
                "autore": autore,
                "mese": mese
            }

            duplicato = False
            for anno in album: #controllo per ogni anno nell'album se esiste una foto
                #che ha come codice il codice da aggiungere. Se esiste cambio il valore
                #del flag
                for i in range(len(album[anno])):
                    if album[anno][i]["codice"] == codice:
                        duplicato = True
            #aggiungo all'album nella lista dell'anno indicato il dizionario
            #che rappresenta la foto nuova, scrivo il file e returno la variabile ma solo
            #se non il codice non è un duplicato
            if duplicato == False:
                album[anno].append(foto_nuova)
                infile.write(f"{codice},{titolo},{autore},{mese},{anno}\n")

                return foto_nuova


    except FileNotFoundError:
        print("None")



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    trovato = False
    for anno in album:
        for i in range(len(album[anno])): #ciclo sui diversi anni
            if codice==album[anno][i]["codice"]:
                trovato = True
                risultato = (f'{album[anno][i]["codice"]}, {album[anno][i]["titolo"]}, {album[anno][i]["autore"]}, '
                      f'{album[anno][i]["mese"]}, {anno}')
                return risultato



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    titoli = [] #lista titoli per anno
    if anno in album:
        lista_foto = album[anno]
        lista_foto.sort(key=itemgetter("titolo"), reverse= False) #ordino per titolo in ordine crescente
        for i in range(len(lista_foto)):
            titoli.append(lista_foto[i]["titolo"])
        return titoli

def main():
    album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
