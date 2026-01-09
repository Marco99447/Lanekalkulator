[README.md](https://github.com/user-attachments/files/24521329/README.md)
# Lånekalkulator 🏦

En profesjonell og brukervennlig lånekalkulator laget i Python med grafisk brukergrensesnitt (GUI). Appen hjelper deg å beregne lånebetingelser, visualisere nedbetalingsplaner og sammenligne din økonomi mot referansebudsjetter fra SIFO 2025.

## Funksjoner ✨

### Lånekalkulator
- **Beregn lånebetingelser** med fleksible parametere
- **Avdragsfrihet** (grace period) uten å forkorte låneperioden
- **Doble gebyrtyper**: Etableringsgebyr (engangs) + Termingebyr (månedlig)
- **5 resultater**: Terminbeløp, terminbeløp etter avdragsfrihet, rentekostnad, gebyrbeløp, og låneperiode

### Nedbetalingsplan
- **Detaljert tabell**: Måned-for-måned og år-for-år oversikt
- **Visualisering**: Stacked bar chart som viser avdrag vs renter per år
- **Interaktivt**: Klikk på årsene for å se månedsdetaljer

### Budsjettberegner
- **SIFO 2025 referansebudsjetter** fra Statistisk sentralbyrå
- **Personlige utgifter**: Mat, klær, pleie, lek basert på kjønn og alder
- **Husholdningsbudsjett**: Dagligvarer, husholdningsartikler, møbler, transport
- **Bilkostnader**: Velg mellom bensinbil og elbil for hver bil
- **Fleksibel familie-størrelse**: Støtte for opptil 6 barn med individuell aldersvalg
- **Visuell sammenligning**: Se din økonomi mot referansebudsjettene

## Installasjon 📦

### For Windows (enkleste måten)
1. Last ned `Lånekalkulator.exe` og `budget_data.py`
2. Legg begge filene i samme mappe
3. Dobbeltklikk på `Lånekalkulator.exe` for å starte

**Krav**: Windows 7 eller nyere (ingen Python-installasjon nødvendig)

### For utviklere (source code)
Hvis du vil modifisere koden, trenger du:
- Python 3.10 eller nyere
- Tkinter (følger med Python som standard)

```bash
# Klon repositoriet
git clone https://github.com/dittbrukernavn/lanekalkulator.git
cd lanekalkulator

# Kjør appen
python lånekalkulator_app.py
```

## Bruk 🎯

### Lånekalkulator
1. Fyll inn lånebeløp, rente, og låneperiode
2. (Valgfritt) Legg inn avdragsfrihet-måneder
3. Legg inn etablerings- og termingebyr
4. Klikk "Beregn" for å se resultater
5. Klikk "Nedbetalingsplan" for detaljert oversikt

### Budsjettberegner
1. Velg antall voksne (kjønn og alder for hver)
2. Legg inn antall barn og deres kjønn/alder
3. Oppgi boligkostnader (kjøp/leie)
4. Legg inn antall biler og type (bensin/el-bil)
5. Se automatisk budsjettberegning basert på SIFO 2025

## Filstruktur 📁

```
Lånekalkulator/
├── Lånekalkulator.exe        # Hovedapplikasjon (Windows)
├── budget_data.py            # SIFO 2025-data (PÅKREVD)
├── lånekalkulator_app.py     # Source code (valgfritt)
├── app_icon.ico              # App-ikon (valgfritt)
└── README.md                 # Denne filen
```

**Viktig**: `budget_data.py` må være i samme mappe som `.exe`-filen for at appen skal fungere.

## Teknologi 🛠️

- **Språk**: Python 3.13
- **GUI**: Tkinter (innebygd i Python)
- **Visualisering**: Matplotlib-inspirert canvas-tegning
- **Data**: SIFO 2025 Referansebudsjett (Statistisk sentralbyrå)
- **Build**: PyInstaller

## Data-kilder 📊

- **SIFO 2025 Referansebudsjett**: Utgiftsbudsjetter for ulike husholdningstyper
- Dekker mat, klær, pleie, transport, og husholdningsutgifter
- Basert på Statistisk sentralbyråets offisielle data

## Lisensiering 📄

Dette prosjektet er Open Source. Du er fri til å:
- Bruke appen privat
- Modifisere koden for dine behov
- Dele det med andre

## Bidrag 🤝

Du er velkommen til å:
- Rapportere bugs og foreslå forbedringer via GitHub Issues
- Forke repositoriet og lage pull requests
- Dele feedback og ideer

## Kontakt 📧

Har du spørsmål eller forslag? Opprett et GitHub Issue i repositoriet.

## Changelog 📝

### v1.0 (Januar 2026)
- Initial release
- Lånekalkulator med avdragsfrihet
- Detaljert nedbetalingsplan med visualisering
- SIFO 2025 budsjettintegrasjon
- Støtte for flexible familiekonfigurasjoner
- Individuell biltype-valg (bensin/el-bil)

---

**Laget med ❤️ for norske låntakere**
