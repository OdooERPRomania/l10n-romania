[
    ("L", "Customer Invoice"),
    ("A", "Supplier Invoice"),
    ("LS", "Special Customer Invoice"),
    ("AS", "Special Supplier Invoice"),
    ("AI", "VAT on Payment Supplier Invoice"),
    ("V", "Inverse Taxation Customer Invoice"),
    ("C", "Inverse Taxation Supplier Invoice"),
    ("N", "Fizical Persons Supplier Invoice"),
]


JOURNAL_COLUMNS = {
    "base_col": {
        "type": "int",
        "tags": [
            "05 - BAZA",
            "07 - BAZA",
            "07_1 - BAZA",  # sale
            "12_1_1 - BAZA",
            "12_1_1 - BAZA",
            "12_1_1 - BAZA",  # sale
        ],
    },
    "tva_col": {
        "type": "int",
        "tags": [
            "05 - TVA",
            "07 - TVA",
            "07_1 - TVA",  # sale
            "12_1_1 - TVA",
            "12_1_1 - TVA",
            "12_1_1 - TVA",  # sale
        ],
    },
    "base_exig": {
        "type": "int",
        "tags": [
            "09 - BAZA",
            "10 - BAZA",
            "11 - BAZA",  # sale
            "24_1 - BAZA",
            "25_1 - BAZA",
            "26_1 - BAZA",  # purchase
        ],
    },  # vat on payment = sum of vat
    "tva_exig": {
        "type": "int",
        "tags": [
            "09 - TVA",
            "10 - TVA",
            "11 - TVA",  # sale
            "24_1 - TVA",
            "25_1 - TVA",
            "26_1 - TVA",  # purchase
        ],
    },  # what was payed = sum of base
    "base_19": {
        "type": "int",
        "tags": ["09 - BAZA", "24_1 - BAZA", "24_2 - BAZA"],  # sale  # purchase
    },
    "tva_19": {
        "type": "int",
        "tags": ["09 - TVA", "24_1 - TVA", "24_2 - TVA"],  # sale  # purchase
    },
    "base_9": {
        "type": "int",
        "tags": ["10 - BAZA", "25_1 - BAZA", "25_2 - BAZA"],  # sale  # purchase
    },
    "tva_9": {
        "type": "int",
        "tags": ["10 - TVA", "25_1 - TVA", "25_2 - TVA"],  # sale  # purchase
    },
    "base_5": {
        "type": "int",
        "tags": ["11 - BAZA", "26_1 - BAZA", "26_2 - BAZA"],  # sale  # purchase
    },
    "tva_5": {
        "type": "int",
        "tags": ["11 - TVA", "26_1 - TVA", "26_2 - TVA"],  # sale  # purchase
    },
    "base_0": {"type": "int", "tags": ["14 - BAZA", "30 - BAZA"]},  # sale  # purchase
    "invers": {"type": "int", "tags": ["13 - BAZA"]},
    "payments": {"type": "list", "tags": []},
    "base_neex": {
        "type": "int",
        "tags": [
            "09 - BAZA",
            "10 - BAZA",
            "11 - BAZA",  # sale
            "24_1 - BAZA",
            "25_1 - BAZA",
            "26_1 - BAZA",  # purchase
        ],
    },  # vat on payment base
    "tva_neex": {
        "type": "int",
        "tags": [
            "09 - TVA",
            "10 - TVA",
            "11 - TVA",  # sale
            "24_1 - TVA",
            "25_1 - TVA",
            "26_1 - TVA",  # purchase
        ],
    },  # vat on payment vat
    "tva_bun": {"type": "int", "tags": []},
    "tva_serv": {"type": "int", "tags": []},
    "neimp": {"type": "int", "tags": ["30 - BAZA"]},
    "others": {"type": "int", "tags": []},
    "scutit1": {"type": "int", "tags": ["14 - BAZA"]},  # cu drept de deducere
    "scutit2": {"type": "int", "tags": ["15 - BAZA"]},  # fara drept de deducere
    "base_ded1": {"type": "int", "tags": ["01 - BAZA"]},  # intracomunitar servicii
    "base_ded2": {"type": "int", "tags": ["03 - BAZA"]},  # intracomunitar bunuri
    "warnings": {"type": "char", "tags": []},
}
