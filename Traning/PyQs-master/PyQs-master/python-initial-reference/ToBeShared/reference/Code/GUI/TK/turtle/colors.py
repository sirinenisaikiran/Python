import math, random
import random 
import matplotlib.pyplot as plt 
from matplotlib import cm 
    
def clamp(x):
    return max(0, min(x, 255))

    
def _init1():
    palette = [(0, 0, 0)]
    redb = 2 * math.pi / (random.randint(0, 128) + 128)
    redc = 256 * random.random()
    greenb = 2 * math.pi / (random.randint(0, 128) + 128)
    greenc = 256 * random.random()
    blueb = 2 * math.pi / (random.randint(0, 128) + 128)
    bluec = 256 * random.random()
    for i in range(256):
        r = clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
        g = clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
        b = clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
        palette.append((r, g, b))
    return palette


 
#initialize 
_palette1 = _init1()
        
def getColor(n, palette=_palette1):
    return palette1[n % 256]


def getColor2( n, palette=None):    
    return (n % 4 * 64, n % 8 * 32, n % 16 * 16)
    
    
    
def _init2(cname=None):
    COLOR_MAPS = [ 'viridis', 'plasma', 'inferno', 'magma',
              'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
                'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
                'hot', 'afmhot', 'gist_heat', 'copper',
                'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
                'Pastel1', 'Pastel2', 'Paired', 'Accent',
                'Dark2', 'Set1', 'Set2', 'Set3',
                'tab10', 'tab20', 'tab20b', 'tab20c',
                'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
                'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
                
    COLOR_MAP = cm.get_cmap(COLOR_MAPS[random.randint(0,len(COLOR_MAPS)-1)])
    if cname:
        COLOR_MAP = cm.get_cmap(cname)
    #my_rgbs =['#ece804','#ece804','#e8e804','#e4e804','#e4e804','#e0e804','#dce804','#dce804','#d8e804','#d4e404','#d4e404','#d0e404','#cce404','#cce404','#c8e404','#c4e404','#c4e404','#c0e404','#bce404','#bce404','#b8e404','#b4e004','#b4e004','#b0e004','#ace004','#ace004','#a8e004','#a4e004','#a4e008','#a0e008','#9ce008','#9ce008','#98dc08','#94dc08','#94dc08','#90dc08','#8cdc08','#8cdc08','#88dc08','#84dc08','#84dc08','#80dc08','#7cdc08','#7cdc08','#78d808','#74d808','#70d808','#70d808','#6cd808','#68d808','#68d808','#64d808','#60d808','#60d808','#5cd808','#58d408','#58d408','#54d408','#50d408','#50d40c','#4cd40c','#48d40c','#48d40c','#44d40c','#40d40c','#40d40c','#3cd40c','#38d00c','#38d00c','#34d00c','#30d00c','#30d00c','#2cd00c','#28d00c','#28d00c','#24d00c','#20d00c','#20d00c','#1ccc0c','#18cc0c','#18cc0c','#14cc0c','#10cc0c','#10cc0c','#0ccc0c','#08cc0c','#08cc0c','#04cc0c','#00cc0c','#00cc0c','#08c81c','#10c428','#18c034','#20bc40','#28bc4c','#30b858','#38b464','#40b070','#48b07c','#44b878','#40bc78','#3cc074','#38c474','#34cc74','#30d070','#2cd470','#28d870','#24d474','#24d478','#20d47c','#20d07c','#1cd080','#1cd084','#1ccc88','#18cc88','#18cc8c','#14c890','#14c890','#14c894','#10c498','#10c49c','#0cc49c','#0cc0a0','#0cc0a4','#08c0a8','#08bca8','#04bcac','#04bcb0','#04bcb0','#08b4ac','#0caca8','#0ca4a8','#109ca4','#1094a4','#148ca0','#1484a0','#187c9c','#18749c','#1c6c98','#1c6498','#205c94','#205494','#244c90','#244490','#283c8c','#28348c','#2c2c88','#2c2888','#302484','#302484','#302480','#302480','#302480','#30247c','#30247c','#30247c','#302478','#302478','#302074','#302074','#302074','#302070','#302070','#302070','#34206c','#34206c','#342068','#342068','#342068','#341c64','#341c64','#341c64','#341c60','#341c60','#341c60','#341c5c','#341c5c','#341c58','#341c58','#341858','#341854','#381854','#381854','#381850','#381850','#38184c','#38184c','#38184c','#381848','#381848','#381448','#381444','#381444','#381444','#381440','#381440','#38143c','#38143c','#3c143c','#3c1438','#3c1038','#3c1038','#3c1034','#3c1034','#3c1030','#3c1030','#3c1030','#3c102c','#3c102c','#3c102c','#3c1028','#3c0c28','#3c0c28','#3c0c24','#3c0c24','#400c20','#400c20','#400c20','#400c1c','#400c1c','#400c1c','#400818','#400818','#400814','#400814','#400814','#400810','#400810','#400810','#40080c','#40080c','#40080c','#440c10','#441010','#441010','#441410','#441414','#481814','#481814','#481c14','#481c18','#482018','#4c2018','#4c2418','#4c241c','#4c281c','#4c2c1c','#502c1c','#503020','#503020','#503420','#503420','#543824','#543824','#543c24','#543c24']
    #my_cmap = matplotlib.colors.ListedColormap(my_rgbs, name='my_name')
    palette = []
    for i in range(256):
        palette.append( tuple([ int(c*255)  for c in COLOR_MAP(i % min(256, COLOR_MAP.N))[:3] ]) ) #only RGB  
    return palette
    
    
#initialize 
_palette2 = _init2()

#call instance with index to get RGBA 
def getColor3(n, palette=_palette2):    
    return palette[n % 256]