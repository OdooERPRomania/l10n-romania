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


dict_tags = {
    "11_1 - TVA": [5, "L", "TVA"],
    "11_1 - BAZA": (5, "L", "BAZA", "11_1 - TVA"),
    "09_1 - BAZA": (19, "L", "BAZA", "09_1 - TVA"),
    "09_1 - TVA": (19, "L", "TVA", "09_1 - BAZA"),
    "09_2 - BAZA": (19, "A", "BAZA", "09_2 - TVA", "%50?"),
    "09_2 - TVA": (19, "A", "TVA", "09_2 - BAZA", "%50?"),
    "10_1 - TVA": (9, "LS", "TVA", "10_1 - BAZA"),
    "10_1 - BAZA": (9, "LS", "BAZA", "10_1 - TVA"),
    "10_2 - TVA": (9, "A", "TVA", "10_2 - BAZA", "%50?"),
    "10_2 - BAZA": (9, "A", "BAZA", "10_2 - TVA", "%50?"),
    "11_1 - BAZA": (5, "LS", "BAZA", "11_1 - TVA"),
    "11_1 - TVA": (5, "LS", "TVA", "09_1 - BAZA"),
    "11_2 - TVA": (5, "A", "TVA", "11_2 - BAZA"),
    "12_1 - BAZA": (19, "V", "BAZA", "12_1 - TVA"),
    "12_1 - TVA": (19, "V", "BAZA", "12_1 - BAZA"),
    "12_2 - BAZA": (9, "V", "BAZA", "12_2 - TVA"),
    "12_2 - TVA": (9, "V", "TVA", "12_2 - BAZA"),
    "12_3 - BAZA": (5, "AS", "BAZA", "12_3 - TVA"),
    "12_3 - TVA": (5, "AS", "TVA", "12_3 - BAZA"),
    "01 - BAZA": (5, "A", "TVA", "01 - BAZA"),
    "01 - TVA": (5, "A", "TVA", "01 - BAZA"),
    "03 - TVA": (5, "A", "TVA", "01 - BAZA"),
    "03 - BAZA": (5, "A", "TVA", "01 - BAZA"),
    "05 - BAZA": (19, "L", "BAZA", "05 - TVA"),
    "05 - TVA": (19, "L", "TVA", "05 - BAZA"),
    "05_1 - BAZA": (9, "AS", "BAZA", "09_1 - TVA"),
    "05_1 - TVA": (9, "AS", "TVA", "09_1 - BAZA"),
    "06 - BAZA": (19, "L", "BAZA", "06 - TVA"),
    "06 - TVA": (19, "L", "TVA", "06 - BAZA"),
    "07 - BAZA": (9, "AS", "BAZA", "07 - TVA"),
    "07 - TVA": (9, "AS", "TVA", "07 - BAZA"),
    "07_1 - BAZA": (9, "AS", "BAZA", "07_1 - TVA"),
    "07_1 - TVA": (9, "AS", "TVA", "07_1 - BAZA"),
    "08 - BAZA": (19, "L", "BAZA", "08 - TVA"),
    "08 - TVA": (19, "L", "TVA", "08 - BAZA"),
    "09 - BAZA": (19, "L", "BAZA", "09 - TVA"),
    "09 - TVA": (19, "L", "TVA", "09 - BAZA"),
    "10 - BAZA": (19, "L", "BAZA", "10 - TVA"),
    "10 - TVA": (19, "L", "TVA", "10 - BAZA"),
    "10_1 - BAZA": (19, "L", "BAZA", "10_1 - TVA"),
    "10_1 - TVA": (19, "L", "TVA", "10_1 - BAZA"),
    "10_2 - BAZA": (19, "L", "BAZA", "10_2 - TVA"),
    "10_2 - TVA": (19, "L", "TVA", "10_2 - BAZA"),
    "13 - BAZA": (0, "V", "BAZA", ""),
    "14 - BAZA": (0, "LS", "BAZA", ""),
    "15 - BAZA": (0, "LS", "BAZA", ""),
    "16 - BAZA": (19, "L", "BAZA", "16 - TVA"),
    "16 - TVA": (19, "L", "TVA", "16 - BAZA"),
    "17 - BAZA": (19, "L", "BAZA", "17 - BAZA"),
    "17 - TVA": (19, "L", "TVA", "17 - BAZA"),
    "18 - BAZA": (19, "L", "BAZA", "18 - TVA"),
    "18 - TVA": (19, "L", "TVA", "18 - BAZA"),
    "20 - BAZA": (19, "AS", "BAZA", "20 - TVA"),
    "20 - TVA": (19, "AS", "TVA", "20 - BAZA"),
    "20_1 - BAZA": (19, "L", "BAZA", "20_1 - TVA"),
    "20_1 - TVA": (19, "L", "TVA", "20_1 - BAZA"),
    "21 - BAZA": (19, "L", "BAZA", "21 - TVA"),
    "21 - TVA": (19, "L", "TVA", "21 - BAZA"),
    "22 - BAZA": (19, "AS", "BAZA", "22 - TVA"),
    "22 - TVA": (19, "AS", "TVA", "22 - BAZA"),
    "22_1 - BAZA": (19, "AS", "BAZA", "22_1 - TVA"),
    "22_1 - TVA": (19, "AS", "TVA", "22_1 - BAZA"),
    "23 - BAZA": (19, "L", "BAZA", "23 - TVA"),
    "23 - TVA": (19, "L", "TVA", "23 - BAZA"),
    "24 - BAZA": (19, "L", "BAZA", "24 - TVA"),
    "24 - TVA": (19, "L", "TVA", "24 - BAZA"),
    "24.1 - BAZA": (19, "A", "BAZA", "24_1 - TVA"),
    "24_1 - BAZA": (19, "A", "BAZA", "24_1 - TVA"),
    "24_1 - TVA": (19, "L", "TVA", "24_1 - BAZA"),
    "24_2 - BAZA": (19, "L", "BAZA", "24_2 - TVA"),
    "24_2 - TVA": (19, "L", "TVA", "24_2 - BAZA"),
    "25 - BAZA": (19, "L", "BAZA", "25 - TVA"),
    "25 - TVA": (19, "L", "TVA", "25 - BAZA"),
    "25_1 - BAZA": (9, "AS", "BAZA", "25_1 - TVA"),
    "25_1 - TVA": (9, "AS", "TVA", "25_1 - BAZA"),
    "25_2 - BAZA": (19, "L", "BAZA", "25_2 - TVA"),
    "25_2 - TVA": (19, "L", "TVA", "25_2 - BAZA"),
    "26 - BAZA": (19, "L", "BAZA", "26 - TVA"),
    "26 - TVA": (19, "L", "TVA", "26 - BAZA"),
    "26_1 - BAZA": (5, "AS", "BAZA", "26_1 - TVA"),
    "26_1 - TVA": (5, "AS", "TVA", "26_1 - BAZA"),
    "26_2 - BAZA": (19, "L", "BAZA", "26_2 - TVA"),
    "26_2 - TVA": (19, "L", "TVA", "26_2 - BAZA"),
    "27 - BAZA": (19, "L", "BAZA", "27 - TVA"),
    "27 - TVA": (19, "L", "TVA", "27 - BAZA"),
    "27_1 - BAZA": (19, "V", "BAZA", "27_1 - TVA"),
    "27_1 - TVA": (19, "V", "TVA", "27_1 - BAZA"),
    "27_2 - BAZA": (9, "V", "BAZA", "27_2 - TVA"),
    "27_2 - TVA": (9, "V", "TVA", "27_2 - BAZA"),
    "27_3 - BAZA": (19, "L", "BAZA", "27_3 - TVA"),
    "27_3 - TVA": (19, "L", "TVA", "27_3 - BAZA"),
    "28 - TVA": (19, "L", "TVA", ""),
    "29 - TVA": (19, "L", "TVA", ""),
    "30 - BAZA": (0, "AS", "BAZA", ""),
    "30_1 - BAZA": (0, "AS", "BAZA", ""),
    "33 - TVA": (19, "L", "TVA", ""),
    "34 - BAZA": (19, "L", "BAZA", "34 - TVA"),
    "34 - TVA": (19, "L", "TVA", "34 - BAZA"),
    "35 - TVA": (19, "L", "TVA", ""),
}
