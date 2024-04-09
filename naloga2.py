import cv2 as cv
import numpy as np
from numba import jit, prange

# Konvolucija funkcija
@jit(nopython=True, parallel=True)
def konvolucija(slika, jedro):
    '''Izvede konvolucijo nad sliko.'''
    visina_slike, sirina_slike, _ = slika.shape
    velikost_jedra = jedro.shape[0]
    polmer_jedra = velikost_jedra // 2
    
    izhodna_slika = np.zeros_like(slika)

    # Gremo skozi vse piksle
    for i in prange(visina_slike):
        for j in prange(sirina_slike):
            vsota = np.zeros(3)
            # Operacija konvolucije
            for m in range(velikost_jedra):
                for n in range(velikost_jedra):
                    x = i + m - polmer_jedra
                    y = j + n - polmer_jedra
                    if 0 <= x < visina_slike and 0 <= y < sirina_slike:
                        vsota += slika[x, y] * jedro[m, n]
            izhodna_slika[i, j] = vsota
    
    return izhodna_slika

# Filtriraj s Sobel jedrom vertikalno
@jit(nopython=True, parallel=True)
def filtriraj_sobel_vertikalno(slika):
    '''Filtrira sliko z vertikalnim Sobel jedrom.'''
    jedro = np.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]], dtype=np.float32)
    
    slika_float32 = slika.astype(np.float32)
    
    filtrirana_slika = konvolucija(slika_float32, jedro)
    
    return filtrirana_slika

# Filtriraj s Sobel jedrom horizontalno
@jit(nopython=True, parallel=True)
def filtriraj_sobel_horizontalno(slika):
    '''Filtrira sliko z horizontalnim Sobel jedrom.'''
    jedro = np.array([[-1, -2, -1],
                      [0, 0, 0],
                      [1, 2, 1]], dtype=np.float32)
    
    slika_float32 = slika.astype(np.float32)
    
    filtrirana_slika = konvolucija(slika_float32, jedro)
    
    return filtrirana_slika

# Zdruzitev vertikalne in horizontalne slike
@jit(nopython=True, parallel=True)
def filtriraj_sobel(slika):
    '''Filtrira sliko z Sobel jedri.'''
    filtrirana_slika_vertikalno = filtriraj_sobel_vertikalno(slika)
    filtrirana_slika_horizontalno = filtriraj_sobel_horizontalno(slika)
    
    combined_image = np.sqrt(np.square(filtrirana_slika_vertikalno) + np.square(filtrirana_slika_horizontalno))
    combined_image = np.clip(combined_image, 0, 255)  # Clip values to [0, 255]
    
    return combined_image.astype(np.uint8)



@jit(nopython=True, parallel=True)
def highlight_strong_gradients(slika):
    '''Find elements with gradient stronger than 100 and change them to red, set everything else to black.'''
    gradient = np.sqrt(np.sum(np.square(slika.astype(np.float32)), axis=2))
    highlighted_image = np.zeros_like(slika)
    
    # Gremo skozi vse piksle
    for i in prange(slika.shape[0]):
        for j in prange(slika.shape[1]):
            if gradient[i, j] > 100:
                highlighted_image[i, j] = [0, 0, 255]  # Nastavimo pixle na rdeco
    
    return highlighted_image

@jit(nopython=True, parallel=True)
def filtriraj_z_gaussovim_jedrom(slika, sigma):
    '''Filtrira sliko z Gaussovim jedrom.'''
    # Preverimo velikost slike
    if len(slika.shape) != 3:
        raise ValueError("Slika mora biti 3D matrika.")
    
    # Velikost slike
    visina_slike, sirina_slike, _ = slika.shape
    
    # Velikost jedra
    velikost_jedra = int(2 * sigma * 2 + 1)
    
    # Polmer jedra
    polmer_jedra = velikost_jedra // 2
    
    # Ustvarimo prazno jedro
    jedro = np.zeros((velikost_jedra, velikost_jedra), dtype=np.float32)
    
    # Izračun gaussovega jedra
    for i in prange(velikost_jedra):
        for j in prange(velikost_jedra):
            x = i - polmer_jedra-1
            y = j - polmer_jedra-1
            jedro[i, j] = (1 / (2 * np.pi * sigma**2)) * np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Normaliziramo jedro
    jedro /= np.sum(jedro)
    
    # Izvedemo konvolucijo
    filtrirana_slika = konvolucija(slika, jedro)
    
    return filtrirana_slika

def resize_image(image):
    return cv.resize(image, (320, 240))


if __name__ == "__main__":
    kamera = cv.VideoCapture(0)
    
    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        while True:
            ret, slika = kamera.read()
            if not ret:
                print("Napaka pri branju slike iz kamere.")
                break
            
            slika = resize_image(slika)
            
            filtrirana_slika_gauss = filtriraj_z_gaussovim_jedrom(slika, sigma=1.25)
            
            filtrirana_slika_sobel = filtriraj_sobel(slika)

            filtrirana_slika_sobel = highlight_strong_gradients(filtrirana_slika_sobel)

            cv.imshow('Izvirna slika', slika)
            
            cv.imshow('Filtrirana slika z Gaussovim jedrom', filtrirana_slika_gauss)
            
            cv.imshow('Filtrirana slika s Sobel jedri', filtrirana_slika_sobel)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
        kamera.release()
        cv.destroyAllWindows()