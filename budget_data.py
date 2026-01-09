"""
Referansebud sjett 2025 - SIFO data
Hentet fra: Referansebudsjettet_2025_norsk.xlsx
"""

# INDIVIDSPESIFIKKE UTGIFTER - basert på kjønn og alder

# MAT & DRIKKE
MAT_BUDGET = {
    "6-11 mnd": 1280,
    "1 år": 1660,
    "2-5": 2210,
    "6-9": 2840,
    "J 10-13": 3440,
    "G 10-13": 3530,
    "J 14-17": 3910,
    "G 14-17": 4470,
    "K 18-30": 4280,
    "K 31-60": 4040,
    "K 61-74": 3720,
    "K 74+": 3360,
    "M 18-30": 5080,
    "M 31-60": 4780,
    "M 61-74": 4200,
    "M 74+": 3900,
    "Gravide/ammende": 4770
}

# KLÆR OG SKO
KLAER_BUDGET = {
    "<1 år": 720,
    "1 år": 1120,
    "2-5": 880,
    "6-9": 990,
    "J 10-13": 860,
    "G 10-13": 840,
    "J 14-17": 1010,
    "G 14-17": 990,
    "K >17": 1070,
    "M >17": 1100
}

# PERSONLIG PLEIE
PLEIE_BUDGET = {
    "<1 år": 510,
    "1-2": 610,
    "3": 360,
    "4-5": 230,
    "6-9": 260,
    "J 10-13": 500,
    "G 10-13": 370,
    "J 14-17": 610,
    "G 14-17": 490,
    "K 18-50": 990,
    "M >17": 800,
    "K >50": 950
}

# LEK OG MEDIEBRUK
LEK_BUDGET = {
    "<1 år": 160,
    "1-2": 380,
    "3-5": 790,
    "6-9": 1230,
    "10-13": 1540,
    "14-17": 1650,
    ">17": 1060
}

# REISEKOSTNADER (pr. mnd - Oslo Ruter 30-dagersbillett feb 2025)
REISE_BUDGET = {
    "6-19": 327,
    "20-66": 985,
    ">66": 493,
    "Student 20-29": 591
}

# HUSHOLDSSPESIFIKKE UTGIFTER - basert på antall personer

# ANDRE DAGLIGVARER (pr. antall personer i hus)
ANDRE_DAGLIGVARER = {
    1: 435,
    2: 500,
    3: 660,
    4: 790,
    5: 900,
    6: 1020,
    7: 1100
}

# HUSHOLDNINGSARTIKLER
HUSHOLDNINGSARTIKLER = {
    1: 585,
    2: 635,
    3: 720,
    4: 915,
    5: 990,
    6: 1070,
    7: 1140
}

# MØBLER
MOBLER = {
    1: 565,
    2: 625,
    3: 760,
    4: 980,
    5: 1145,
    6: 1375,
    7: 1565
}

# MEDIEBRUK OG FRITID (hele husholdningen)
MEDIEBRUK_FRITID = {
    1: 2520,
    2: 2560,
    3: 2700,
    4: 2790,
    5: 2820,
    6: 2850,
    7: 2850
}

# BILKOSTNADER (Drift og vedlikehold, pr. måned)
BILKOSTNADER = {
    "Bensinbil": {
        "1-4 personer": 3300,
        "5-7 personer": 4990
    },
    "El-bil": {
        "1-4 personer": 2195,
        "5-7 personer": 3015
    }
}

# Aldersintervaller for voksne (Kvinner/Menn)
ADULT_AGE_GROUPS = {
    "18-30": "K 18-30",  # Vil bli M/K 18-30 basert på valg
    "31-60": "K 31-60",
    "61-74": "K 61-74",
    "74+": "K 74+"
}

# Aldersintervaller for barn
CHILD_AGE_GROUPS = {
    "6-11 mnd": "6-11 mnd",
    "1 år": "1 år",
    "2-5": "2-5",
    "6-9": "6-9",
    "10-13": "J 10-13",  # Vil bli J/G 10-13 basert på kjønn
    "14-17": "J 14-17"   # Vil bli J/G 14-17 basert på kjønn
}

# Hjelpe-funksjoner for å hente riktig verdi basert på kjønn og alder

def get_mat_budget(alder, kjønn="K"):
    """Hent mat-budget basert på alder og kjønn"""
    if alder in MAT_BUDGET:
        return MAT_BUDGET[alder]
    
    # Hvis det er voksen, bytt K/M
    key = alder.replace("K ", f"{kjønn} ").replace("M ", f"{kjønn} ")
    return MAT_BUDGET.get(key, 0)

def get_klaer_budget(alder, kjønn="K"):
    """Hent klær-budget basert på alder"""
    if alder in ["<1 år", "1 år", "2-5", "6-9"]:
        return KLAER_BUDGET.get(alder, 0)
    
    # Bare K >17 eller M >17 for voksne
    if alder in KLAER_BUDGET:
        return KLAER_BUDGET[alder]
    
    key = f"{kjønn} >17"
    return KLAER_BUDGET.get(key, 0)

def get_pleie_budget(alder, kjønn="K"):
    """Hent pleie-budget basert på alder"""
    if alder in ["<1 år", "1-2", "3", "4-5", "6-9"]:
        return PLEIE_BUDGET.get(alder, 0)
    
    if alder in PLEIE_BUDGET:
        return PLEIE_BUDGET[alder]
    
    # For voksne
    if kjønn == "K":
        if int(alder.split("-")[0]) <= 50:
            return PLEIE_BUDGET.get("K 18-50", 0)
        else:
            return PLEIE_BUDGET.get("K >50", 0)
    else:
        return PLEIE_BUDGET.get("M >17", 0)

def get_lek_budget(alder):
    """Hent lek-budget basert på alder"""
    if alder in ["<1 år", "1-2", "3-5", "6-9"]:
        return LEK_BUDGET.get(alder, 0)
    elif alder in ["10-13", "14-17"]:
        return LEK_BUDGET.get(alder, 0)
    else:
        return LEK_BUDGET.get(">17", 0)

def get_household_size_category(num_persons):
    """Konverter antall personer til kategori (1-7)"""
    return min(num_persons, 7)  # Max 7 i tabellene

if __name__ == "__main__":
    print("Budget data loaded successfully!")
    print(f"Mat K 18-30: {get_mat_budget('K 18-30', 'K')}")
    print(f"Mat M 18-30: {get_mat_budget('M 18-30', 'M')}")
