import skyfield.named_stars

HEADER = """
############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
###########################################################

# this file is auto generated

import skyfield.starlib


class AlignStar:

    # alignment star from hipparcos catatlogue, selection is equivalent to skyfield

    alignStar = dict()

    # now the stars
    
"""

FOOTER = """
    def __init__(self):
        pass

    def __getitem__(self, item):
        if item in self.star:
            return self.star[item]

    def __missing__(self, key):
        return None

    def __iter__(self):
        return iter(self.star)

    def keys(self):
        return self.star.keys()

    def items(self):
        return self.star.items()

    def values(self):
        return self.star.values()


if __name__ == "__main__":

    star = AlignStar()
    for name, value in star.items():
        print(name, value.ra.hours, value.dec.degrees)
"""

named_star_dict = {
    'Achernar': 7588,
    'Acrux': 60718,
    'Adhara': 33579,
    'Agena': 68702,
    'Albireo': 95947,
    'Alcor': 65477,
    'Aldebaran': 21421,
    'Alderamin': 105199,
    'Algenib': 15863,
    'Algieba': 50583,
    'Algol': 14576,
    'Alhena': 31681,
    'Alioth': 62956,
    'Alkaid': 67301,
    'Almach': 9640,
    'Alnair': 109268,
    'Alnilam': 26311,
    'Alnitak': 26727,
    'Alphard': 46390,
    'Alphecca': 76267,
    'Alpheratz': 677,
    'Altair': 97649,
    'Aludra': 35904,
    'Ankaa': 2081,
    'Antares': 80763,
    'Arcturus': 69673,
    'Arided': 102098,
    'Aridif': 102098,
    'Aspidiske': 45556,
    'Atria': 82273,
    'Avior': 41037,
    'Becrux': 62434,
    'Bellatrix': 25336,
    'Benetnash': 67301,
    'Betelgeuse': 27989,
    'Birdun': 66657,
    'Canopus': 30438,
    'Capella': 24608,
    'Caph': 746,
    'Castor': 36850,
    'Deneb': 102098,
    'Deneb Kaitos': 3419,
    'Denebola': 57632,
    'Diphda': 3419,
    'Dschubba': 78401,
    'Dubhe': 54061,
    'Durre Menthor': 8102,
    'Elnath': 25428,
    'Enif': 107315,
    'Etamin': 87833,
    'Fomalhaut': 113368,
    'Foramen': 93308,
    'Gacrux': 61084,
    'Gemma': 76267,
    'Gienah': 102488,
    'Girtab': 86228,
    'Gruid': 112122,
    'Hadar': 68702,
    'Hamal': 9884,
    "Herschel's Garnet Star": 107259,
    'Izar': 72105,
    'Kaus Australis': 90185,
    'Kochab': 72607,
    'Koo She': 42913,
    'Marchab': 113963,
    'Marfikent': 71352,
    'Markab': 45941,
    'Megrez': 59774,
    'Men': 71860,
    'Menkalinan': 28360,
    'Menkent': 68933,
    'Merak': 53910,
    'Miaplacidus': 45238,
    'Mimosa': 62434,
    'Mintaka': 25930,
    'Mira': 10826,
    'Mirach': 5447,
    'Mirfak': 15863,
    'Mirzam': 30324,
    'Mizar': 65378,
    'Muhlifein': 61932,
    'Murzim': 30324,
    'Naos': 39429,
    'Nunki': 92855,
    'Peacock': 100751,
    'Phad': 58001,
    'Phecda': 58001,
    'Polaris': 11767,
    'Pollux': 37826,
    'Procyon': 37279,
    'Ras Alhague': 86032,
    'Rasalhague': 86032,
    'Regor': 39953,
    'Regulus': 49669,
    'Rigel': 24436,
    'Rigel Kent': 71683,
    'Rigil Kentaurus': 71683,
    'Sabik': 84012,
    'Sadira': 16537,
    'Sadr': 100453,
    'Saiph': 27366,
    'Sargas': 86228,
    'Scheat': 113881,
    'Schedar': 3179,
    'Scutulum': 45556,
    'Shaula': 85927,
    'Sirius': 32349,
    'Sirrah': 677,
    'South Star': 104382,
    'Spica': 65474,
    'Suhail': 44816,
    'Thuban': 68756,
    'Toliman': 71683,
    'Tseen She': 93308,
    'Tsih': 4427,
    'Turais': 45556,
    'Vega': 91262,
    'Wei': 82396,
    'Wezen': 34444,
}

with open('alignStar.py', 'w') as f:
    f.write(HEADER)
    for name in named_star_dict:
        starH = skyfield.named_stars.NamedStar(name)
        ra_hours = starH.ra.hours
        dec_degrees = starH.dec.degrees
        ra_mas_per_year = starH.ra_mas_per_year
        dec_mas_per_year = starH.dec_mas_per_year
        parallax_mas = starH.parallax_mas
        radial_km_per_s = starH.radial_km_per_s
        lineA = 'alignStar["{0}"] = skyfield.starlib.Star(ra_hours={1}, dec_degrees={2}, ra_mas_per_year={3}'.format(
            name, ra_hours, dec_degrees, ra_mas_per_year
        )
        lineB = ', dec_mas_per_year={0}, parallax_mas={1}, radial_km_per_s={2})\n'.format(
            dec_mas_per_year, parallax_mas, radial_km_per_s
        )
        print(lineA + lineB)
        f.write('    ' + lineA + lineB)
    f.write(FOOTER)


