
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
import skyfield.starlib


class AlignStars:
    """
    The class AlignStars provides a list of selected stars from hipparcos catalogue
    dedicated for the polar alignment routine of 10 micron mounts. The format
    of the alignment stars stored in 'Star' class defined in skyfield.starlib

    The star data is defined in an ICRF and should not be altered.

    You could access the alignment stars via iterator

        >>> alignStars = AlignStars()
        >>> for name, star in alignStars.items():
        >>>     print(name, star)

    or you could extract a dedicated star with

        >>> print(alignStars.getStars('Sirius'))

    """

    version = '0.1'

    # prepare the data og the stars
    _s = {
        'Achernar': [1.6285684909910512, -57.23675748604603, 88.02, -40.08, 22.68, -40.08, 22.68],
        'Acrux': [12.443304389488853, -63.0990916619562, -35.37, -14.73, 10.17, -14.73, 10.17],
        'Adhara': [6.977096787783971, -28.972083744027586, 2.63, 2.29, 7.57, 2.29, 7.57],
        'Agena': [14.063723467348478, -60.373039309617674, -33.96, -25.06, 6.21, -25.06, 6.21],
        'Albireo': [19.512022385341623, 27.959681115970845, -7.09, -5.63, 8.46, -5.63, 8.46],
        'Alcor': [13.420427210362131, 54.98795766532296, 120.35, -16.94, 40.19, -16.94, 40.19],
        'Aldebaran': [4.598677406767971, 16.509301389939786, 62.78, -189.36, 50.09, -189.36, 50.09],
        'Alderamin': [21.309658745909516, 62.58557261068296, 149.91, 48.27, 66.84, 48.27, 66.84],
        'Algenib': [3.4053806529520334, 49.86117959121446, 24.11, -26.01, 5.51, -26.01, 5.51],
        'Algieba': [10.332876236967754, 19.841488734870072, 310.77, -152.88, 25.96, -152.88, 25.96],
        'Algol': [3.1361476567909103, 40.955647699999744, 2.39, -1.44, 35.14, -1.44, 35.14],
        'Alhena': [6.628528082759717, 16.39925216722216, -2.04, -66.92, 31.12, -66.92, 31.12],
        'Alioth': [12.900485951888628, 55.959821158352696, 111.74, -8.99, 40.3, -8.99, 40.3],
        'Alkaid': [13.792343787984251, 49.31326505967427, -121.23, -15.56, 32.39, -15.56, 32.39],
        'Almach': [2.0649869643468484, 42.329724726162844, 43.08, -50.85, 9.19, -50.85, 9.19],
        'Alnair': [22.13721818655977, -46.96097543257332, 127.6, -147.91, 32.16, -147.91, 32.16],
        'Alnilam': [5.6035592894883175, -1.2019198263888866, 1.49, -1.06, 2.43, -1.06, 2.43],
        'Alnitak': [5.679313094899547, -1.9425722363888611, 3.99, 2.54, 3.99, 2.54, 3.99],
        'Alphard': [9.459789798348773, -8.658602534026127, -14.49, 33.25, 18.4, 33.25, 18.4],
        'Alphecca': [15.578130032315757, 26.714693020735133, 120.38, -89.44, 43.65, -89.44, 43.65],
        'Alpheratz': [0.13979404756006997, 29.090431990444202, 135.68, -162.95, 33.6, -162.95, 33.6],
        'Altair': [19.84638861051789, 8.868321984070757, 536.82, 385.54, 194.44, 385.54, 194.44],
        'Aludra': [7.401584037342451, -29.303103602499593, -3.76, 6.66, 1.02, 6.66, 1.02],
        'Ankaa': [0.43806971414947443, -42.305981509124614, 232.76, -353.64, 42.14, -353.64, 42.14],
        'Antares': [16.490128030847767, -26.432002493191803, -10.16, -23.21, 5.4, -23.21, 5.4],
        'Arcturus': [14.261020006808682, 19.182410295790085, -1093.45, -1999.4, 88.85, -1999.4, 88.85],
        'Arided': [20.6905318725771, 45.28033799736099, 1.56, 1.55, 1.01, 1.55, 1.01],
        'Aridif': [20.6905318725771, 45.28033799736099, 1.56, 1.55, 1.01, 1.55, 1.01],
        'Aspidiske': [9.284835187284724, -59.27522928538525, -19.03, 13.11, 4.71, 13.11, 4.71],
        'Atria': [16.811081909109944, -69.02771504384603, 17.85, -32.92, 7.85, -32.92, 7.85],
        'Avior': [8.375232106994085, -59.50948306772156, -25.34, 22.72, 5.16, 22.72, 5.16],
        'Becrux': [12.795350870157481, -59.688763619517, -48.24, -12.82, 9.25, -12.82, 9.25],
        'Bellatrix': [5.418850850757774, 6.3497022322217855, -8.75, -13.28, 13.42, -13.28, 13.42],
        'Benetnash': [13.792343787984251, 49.31326505967427, -121.23, -15.56, 32.39, -15.56, 32.39],
        'Betelgeuse': [5.919529239737559, 7.407062735828328, 27.33, 10.86, 7.63, 10.86, 7.63],
        'Birdun': [13.664794000596656, -53.46639377679071, -14.6, -12.79, 8.68, -12.79, 8.68],
        'Canopus': [6.3991971866540736, -52.69566045872297, 19.99, 23.67, 10.43, 23.67, 10.43],
        'Capella': [5.278155293267133, 45.99799110650121, 75.52, -427.13, 77.29, -427.13, 77.29],
        'Caph': [0.15296807541656848, 59.14977959552322, 523.39, -180.42, 59.89, -180.42, 59.89],
        'Castor': [7.576628556311226, 31.888276288912298, -206.33, -148.18, 63.27, -148.18, 63.27],
        'Deneb': [20.6905318725771, 45.28033799736099, 1.56, 1.55, 1.01, 1.55, 1.01],
        'Deneb Kaitos': [0.7264919601096897, -17.98660459562076, 232.79, 32.71, 34.04, 32.71, 34.04],
        'Denebola': [11.817660437393638, 14.57206031805155, -499.02, -113.78, 90.16, -113.78, 90.16],
        'Diphda': [0.7264919601096897, -17.98660459562076, 232.79, 32.71, 34.04, 32.71, 34.04],
        'Dschubba': [16.005557294713373, -22.621709927498383, -8.67, -36.9, 8.12, -36.9, 8.12],
        'Dubhe': [11.062130192490221, 61.75103320112995, -136.46, -35.25, 26.38, -35.25, 26.38],
        'Durre Menthor': [1.734467475849155, -15.937480061772153, -1721.82, 854.07, 274.17, 854.07, 274.17],
        'Elnath': [5.438198166101953, 28.607450008595883, 23.28, -174.22, 24.89, -174.22, 24.89],
        'Enif': [21.736432809504855, 9.875011264158582, 30.02, 1.38, 4.85, 1.38, 4.85],
        'Etamin': [17.943436075499083, 51.48889498568973, -8.52, -23.05, 22.1, -23.05, 22.1],
        'Fomalhaut': [22.96084624820144, -29.62223615265622, 329.22, -164.22, 130.08, -164.22, 130.08],
        'Foramen': [19.0049327596155, -55.015580999305364, 1.69, 18.35, 4.79, 18.35, 4.79],
        'Gacrux': [12.519433139224041, -57.11321168868774, 27.94, -264.33, 37.09, -264.33, 37.09],
        'Gemma': [15.578130032315757, 26.714693020735133, 120.38, -89.44, 43.65, -89.44, 43.65],
        'Gienah': [20.770189648487424, 33.97025609948278, 356.16, 330.28, 45.26, 330.28, 45.26],
        'Girtab': [17.621980723925383, -42.99782385902602, 6.06, -0.95, 11.99, -0.95, 11.99],
        'Gruid': [22.71112518766103, -46.88457690079192, 135.68, -4.51, 19.17, -4.51, 19.17],
        'Hadar': [14.063723467348478, -60.373039309617674, -33.96, -25.06, 6.21, -25.06, 6.21],
        'Hamal': [2.119557528835421, 23.46242312710268, 190.73, -145.77, 49.48, -145.77, 49.48],
        'Herschels Garnet Star': [21.72512801211178, 58.78004607999765, 5.24, -2.88, 0.62, -2.88, 0.62],
        'Izar': [14.749782695446205, 27.074222441043503, -50.65, 20.0, 15.55, 20.0, 15.55],
        'Kaus Australis': [18.402866200757806, -34.38461611036131, -39.61, -124.05, 22.55, -124.05, 22.55],
        'Kochab': [14.845090670444478, 74.15550490772729, -32.29, 11.91, 25.79, 11.91, 25.79],
        'Koo She': [8.745062881287438, -54.70882108799522, 28.78, -104.14, 40.9, -104.14, 40.9],
        'Marchab': [23.079348272961244, 15.205264415503251, 61.1, -42.56, 23.36, -42.56, 23.36],
        'Marfikent': [14.591784390419466, -42.157824467164026, -35.31, -32.44, 10.57, -32.44, 10.57],
        'Markab': [9.36856064476279, -55.010667990547084, -10.72, 11.24, 6.05, 11.24, 6.05],
        'Megrez': [12.257100034120432, 57.03261690178644, 103.56, 7.81, 40.05, 7.81, 40.05],
        'Men': [14.698821005377841, -47.388200138030484, -21.15, -24.22, 5.95, -24.22, 5.95],
        'Menkalinan': [5.992145259211346, 44.94743278094737, -56.41, -0.88, 39.72, -0.88, 39.72],
        'Menkent': [14.111374571622669, -36.36995445156714, -519.29, -517.87, 53.52, -517.87, 53.52],
        'Merak': [11.030687999605183, 56.382426786427374, 81.66, 33.74, 41.07, 33.74, 41.07],
        'Miaplacidus': [9.219993190723619, -69.71720773472705, -157.66, 108.91, 29.34, 108.91, 29.34],
        'Mimosa': [12.795350870157481, -59.688763619517, -48.24, -12.82, 9.25, -12.82, 9.25],
        'Mintaka': [5.533444645272205, -0.2990920388888882, 1.67, 0.56, 3.56, 0.56, 3.56],
        'Mira': [2.3224424114388684, -2.9776426194441377, 10.33, -239.48, 7.79, -239.48, 7.79],
        'Mirach': [1.162200995068799, 35.620557697611176, 175.59, -112.23, 16.36, -112.23, 16.36],
        'Mirfak': [3.4053806529520334, 49.86117959121446, 24.11, -26.01, 5.51, -26.01, 5.51],
        'Mirzam': [6.3783292456834735, -17.955917722360915, -3.45, -0.47, 6.53, -0.47, 6.53],
        'Mizar': [13.398761920264775, 54.92536175239315, 121.23, -22.01, 41.73, -22.01, 41.73],
        'Muhlifein': [12.691955167774646, -48.95988844458953, -187.28, -1.2, 25.01, -1.2, 25.01],
        'Murzim': [6.3783292456834735, -17.955917722360915, -3.45, -0.47, 6.53, -0.47, 6.53],
        'Naos': [8.059735187852958, -40.00314769954223, -30.82, 16.77, 2.33, 16.77, 2.33],
        'Nunki': [18.921090477553655, -26.296722248745102, 13.87, -52.65, 14.54, -52.65, 14.54],
        'Peacock': [20.42746050896483, -56.73509010235645, 7.71, -86.15, 17.8, -86.15, 17.8],
        'Phad': [11.897179848125406, 53.69476008418518, 107.76, 11.16, 38.99, 11.16, 38.99],
        'Phecda': [11.897179848125406, 53.69476008418518, 107.76, 11.16, 38.99, 11.16, 38.99],
        'Polaris': [2.5303010234979415, 89.26410950742917, 44.22, -11.74, 7.56, -11.74, 7.56],
        'Pollux': [7.755263988502078, 28.026198615229106, -625.69, -45.95, 96.74, -45.95, 96.74],
        'Procyon': [7.655032867306519, 5.224993063414227, -716.57, -1034.58, 285.93, -1034.58, 285.93],
        'Ras Alhague': [17.582241821699995, 12.560034773888612, 110.08, -222.61, 69.84, -222.61, 69.84],
        'Rasalhague': [17.582241821699995, 12.560034773888612, 110.08, -222.61, 69.84, -222.61, 69.84],
        'Regor': [8.158875066792271, -47.336587707498026, -5.93, 9.9, 3.88, 9.9, 3.88],
        'Regulus': [10.139530740152827, 11.967207063348102, -249.4, 4.91, 42.09, 4.91, 42.09],
        'Rigel': [5.242297874807085, -8.201640551111085, 1.87, -0.56, 4.22, -0.56, 4.22],
        'Rigel Kent': [14.66013772257702, -60.83397468139249, -3678.19, 481.84, 742.12, 481.84, 742.12],
        'Rigil Kentaurus': [14.66013772257702, -60.83397468139249, -3678.19, 481.84, 742.12, 481.84, 742.12],
        'Sabik': [17.172968701426836, -15.724910226225411, 41.16, 97.65, 38.77, 97.65, 38.77],
        'Sadira': [3.54884560600934, -9.458262154728086, -976.44, 17.97, 310.75, 17.97, 310.75],
        'Sadr': [20.37047274661545, 40.25667923958307, 2.43, -0.93, 2.14, -0.93, 2.14],
        'Saiph': [5.795941348777099, -9.669604776666644, 1.55, -1.2, 4.52, -1.2, 4.52],
        'Sargas': [17.621980723925383, -42.99782385902602, 6.06, -0.95, 11.99, -0.95, 11.99],
        'Scheat': [23.062904867258066, 28.082789087780267, 187.76, 137.61, 16.37, 137.61, 16.37],
        'Schedar': [0.6751223652032042, 56.53733108882995, 50.36, -32.17, 14.27, -32.17, 14.27],
        'Scutulum': [9.284835187284724, -59.27522928538525, -19.03, 13.11, 4.71, 13.11, 4.71],
        'Shaula': [17.56014444045273, -37.103821145135804, -8.9, -29.95, 4.64, -29.95, 4.64],
        'Sirius': [6.752477025765419, -16.716115819270435, -546.01, -1223.08, 379.21, -1223.08, 379.21],
        'Sirrah': [0.13979404756006997, 29.090431990444202, 135.68, -162.95, 33.6, -162.95, 33.6],
        'South Star': [21.146346010469216, -88.95649899670357, 25.96, 5.02, 12.07, 5.02, 12.07],
        'Spica': [13.419883133995869, -11.161322031509407, -42.5, -31.73, 12.44, -31.73, 12.44],
        'Suhail': [9.13326623836911, -43.432589351640374, -23.21, 14.28, 5.69, 14.28, 5.69],
        'Thuban': [14.073152714322651, 64.37585051090666, -56.52, 17.19, 10.56, 17.19, 10.56],
        'Toliman': [14.66013772257702, -60.83397468139249, -3678.19, 481.84, 742.12, 481.84, 742.12],
        'Tseen She': [19.0049327596155, -55.015580999305364, 1.69, 18.35, 4.79, 18.35, 4.79],
        'Tsih': [0.9451477026042057, 60.7167403752173, 25.65, -3.82, 5.32, -3.82, 5.32],
        'Turais': [9.284835187284724, -59.27522928538525, -19.03, 13.11, 4.71, 13.11, 4.71],
        'Vega': [18.615649007099478, 38.78369179582599, 201.02, 287.46, 128.93, 287.46, 128.93],
        'Wei': [16.836059159468615, -34.293231713088886, -611.83, -255.87, 49.85, -255.87, 49.85],
        'Wezen': [7.139856737879104, -26.39319966624981, -2.75, 3.33, 1.82, 3.33, 1.82],
    }

    # load the data in an appropriate class dict for all instances
    star = dict()
    for name, values in _s.items():
        star[name] = skyfield.starlib.Star(
            ra_hours=values[0],
            dec_degrees=values[1],
            ra_mas_per_year=values[2],
            dec_mas_per_year=values[3],
            parallax_mas=values[4],
            radial_km_per_s=values[5],
        )

    # delete raw database
    del _s

    def __init__(self):
        pass

    def __iter__(self):
        return iter(self.star)

    def keys(self):
        return self.star.keys()

    def items(self):
        return self.star.items()

    def values(self):
        return self.star.values()

    def getStar(self, name):
        """
        getStar gives you the data for the named star if present

        :param name:    name of the selected stars
        :return:        skyfield.starlib.Star class of named star
        """
        if name in self.star:
            return self.star[name]
        else:
            return None


if __name__ == "__main__":

    stars = AlignStars()

    print(stars.getStar('Sirius'))

    print(stars.__doc__)

    print(stars.version)