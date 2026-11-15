"""Props nuevos para Marte, con la paleta de los props de la Luna: extractor de oxigeno y taladro de hielo."""
import sys, os
from PIL import Image

P = {'crema': '#f6f1e4', 'crema2': '#d9d2c0', 'cafe': '#8f8672', 'gris': '#6a6f7d', 'gris2': '#a9adb8',
     'osc': '#3d4252', 'neg': '#12141f', 'neg2': '#161b2b', 'oro': '#d39528', 'oro2': '#f6d277', 'oro3': '#7d5210',
     'cian': '#62e4e0', 'cian2': '#2a9e9b', 'ama': '#f2b134', 'ama2': '#ffe08a', 'nar': '#f08a5d', 'hielo': '#a8e4f0', 'hielo2': '#ccebe2'}


def lienzo(w, h):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def rect(im, x, y, w, h, c):
    col = tuple(int(P[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= xx < im.width and 0 <= yy < im.height: im.putpixel((xx, yy), col)


def base(im, x, w, y):
    """plataforma gris con remaches, como la de los modulos lunares"""
    rect(im, x, y, w, 4, 'gris'); rect(im, x, y, w, 1, 'gris2'); rect(im, x, y + 3, w, 1, 'osc')
    for k in range(x + 3, x + w - 2, 6): rect(im, k, y + 1, 1, 1, 'neg')


def extractor():
    # caja dorada (como MOXIE) + tanque crema de oxigeno + toma de aire
    im = lienzo(56, 44)
    base(im, 0, 56, 40)
    # caja dorada con laminas
    rect(im, 3, 16, 26, 24, 'neg'); rect(im, 4, 17, 24, 22, 'oro')
    for y in range(18, 38, 3): rect(im, 5, y, 22, 1, 'oro2' if y % 2 else 'oro3')
    for y in range(17, 39):
        for x in range(4, 28):
            if (x * 7 + y * 13) % 17 == 0: rect(im, x, y, 1, 1, 'oro2')
    rect(im, 8, 22, 14, 8, 'neg2'); rect(im, 9, 23, 12, 6, 'osc')
    rect(im, 10, 25, 2, 2, 'cian'); rect(im, 13, 25, 2, 2, 'cian'); rect(im, 16, 24, 4, 1, 'cian2'); rect(im, 16, 27, 3, 1, 'cian2')
    # toma de aire (rejilla) arriba
    rect(im, 8, 10, 16, 6, 'neg'); rect(im, 9, 11, 14, 4, 'gris')
    for x in range(10, 22, 2): rect(im, x, 11, 1, 4, 'osc')
    rect(im, 15, 6, 2, 4, 'gris2'); rect(im, 13, 5, 6, 1, 'gris2')
    # tubo al tanque
    rect(im, 28, 26, 6, 2, 'gris2'); rect(im, 28, 28, 6, 1, 'osc')
    # tanque vertical
    rect(im, 34, 8, 18, 32, 'neg'); rect(im, 35, 9, 16, 30, 'crema2'); rect(im, 36, 10, 6, 28, 'crema')
    rect(im, 35, 9, 16, 1, 'crema'); rect(im, 37, 7, 12, 2, 'neg'); rect(im, 38, 7, 10, 1, 'crema2')
    rect(im, 35, 22, 16, 3, 'cian'); rect(im, 35, 25, 16, 1, 'cian2')
    rect(im, 42, 14, 6, 5, 'neg2'); rect(im, 43, 15, 1, 3, 'cian'); rect(im, 45, 15, 2, 1, 'cian'); rect(im, 45, 17, 2, 1, 'cian')   # "O2"
    rect(im, 49, 4, 1, 4, 'gris2'); rect(im, 48, 3, 3, 1, 'nar')
    return im


def taladro():
    # torre de perforacion con broca y deposito de agua
    im = lienzo(48, 76)
    base(im, 0, 48, 72)
    # torre (celosia)
    for y in range(8, 72):
        rect(im, 14, y, 1, 1, 'gris2'); rect(im, 29, y, 1, 1, 'gris')
        if y % 8 == 0: rect(im, 14, y, 16, 1, 'gris')
        k = (y % 8)
        rect(im, 14 + k * 2, y, 1, 1, 'osc')
    rect(im, 11, 4, 22, 5, 'neg'); rect(im, 12, 5, 20, 3, 'ama')
    for x in range(12, 32, 4): rect(im, x, 5, 2, 3, 'neg2')
    rect(im, 21, 9, 2, 6, 'gris2')
    # motor
    rect(im, 17, 15, 10, 9, 'neg'); rect(im, 18, 16, 8, 7, 'crema2'); rect(im, 18, 16, 8, 2, 'crema'); rect(im, 20, 19, 4, 2, 'nar')
    # broca
    for y in range(24, 70):
        rect(im, 21, y, 2, 1, 'gris2' if (y // 2) % 2 else 'gris')
    rect(im, 20, 68, 4, 2, 'osc')
    # deposito de agua al lado
    rect(im, 32, 44, 15, 28, 'neg'); rect(im, 33, 45, 13, 26, 'crema2'); rect(im, 34, 46, 4, 24, 'crema')
    rect(im, 33, 56, 13, 14, 'hielo'); rect(im, 33, 56, 13, 1, 'hielo2'); rect(im, 39, 50, 5, 3, 'neg2')
    rect(im, 29, 50, 4, 2, 'gris2')
    # panel de control a la izquierda
    rect(im, 1, 50, 12, 22, 'neg'); rect(im, 2, 51, 10, 20, 'gris'); rect(im, 3, 53, 8, 6, 'neg2')
    rect(im, 4, 55, 2, 2, 'cian'); rect(im, 7, 54, 3, 1, 'ama'); rect(im, 7, 57, 3, 1, 'cian2')
    return im


if __name__ == '__main__':
    d = sys.argv[1]; os.makedirs(d, exist_ok=True)
    extractor().save(os.path.join(d, 'extractor.png'))
    taladro().save(os.path.join(d, 'taladro.png'))
    print('ok')
