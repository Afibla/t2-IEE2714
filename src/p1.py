import numpy as np
from scipy.signal import convolve2d

def imagen_sintetica(size=256):
    # imagen de fondo 256x256, intensidad 0.15
    imagen = np.full((size, size), 0.15, dtype=np.float64)

    # cuadrado centrado 128x128, intensidad 0.45
    imagen[size//4:size*3//4, size//4:size*3//4] = 0.45

    # circulo centrado radio 32, intensidad 0.80
    yy, xx = np.ogrid[-size//2:size//2, -size//2:size//2]
    mask_circulo = xx**2 + yy**2 <= (size//8)**2
    imagen[mask_circulo] = 0.80

    # mascaras excluyentes
    mask_fondo = (imagen == 0.15)
    # cuadrado excluye circulo
    mask_cuadrado = (imagen == 0.45) & ~mask_circulo
    mask_circulo = (imagen == 0.80)

    return imagen, mask_fondo, mask_cuadrado, mask_circulo

# simulacion ruido poisson imagen ideal x, y =poisson(N*x)/N con N=40
np.random.seed(2714)
N = 40
x, mask_fondo, mask_cuadrado, mask_circulo = imagen_sintetica()
y = np.random.poisson(N * x).astype(np.float64) / N

def kernel_gaussiano(sigma=1.0):
    radio = int(np.ceil(3* sigma))
    ax = np.arange(-radio, radio + 1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)
    return kernel

def rmse(ref, est, mask=None):
    if mask is not None:
        ref = ref[mask]
        est = est[mask]
    return np.sqrt(np.mean((ref - est) ** 2))


def filtro_gaussiano(imagen, sigma=1.0):
    if sigma <= 0:
        return imagen.copy()
    kernel = kernel_gaussiano(sigma)
    # convolucion como en colab curso
    return convolve2d(imagen, kernel, mode='same', boundary='symm')

# interpolación lineal saturada para mapeo de sigma basado en experimentos
def funcion_mapeo_sigma(mu, int_ref, sigmas_ref):
    return np.interp(mu, int_ref, sigmas_ref)

def filtro_gaussiano_adaptativo(img, mapa_s, num_niveles=25):
    # diferencia de sigma pequeña, se aplica filtro gaussiano con sigma constante
    s_min, s_max = mapa_s.min(), mapa_s.max()
    if abs(s_max - s_min) < 1e-6:
        return filtro_gaussiano(img, s_min)

    # aplicar el filtro gaussiano para cada nivel de sigma y almacenar en un banco
    grid_sigmas = np.linspace(s_min, s_max, num_niveles)
    banco = np.stack([filtro_gaussiano(img, s) for s in grid_sigmas], axis=0)

    # mapeo de sigma(x,y) a índices de banco y pesos para interpolación lineal
    idx_float = (mapa_s - s_min) / (s_max - s_min) * (num_niveles - 1)
    idx_low = np.clip(np.floor(idx_float).astype(int), 0, num_niveles - 1)
    idx_high = np.clip(np.ceil(idx_float).astype(int), 0, num_niveles - 1)
    
    w_high = idx_float - idx_low
    w_low = 1.0 - w_high

    # mezcla de imágenes filtradas usando los pesos calculados
    H, W = img.shape
    y_g, x_g = np.ogrid[:H, :W]
    img_low = banco[idx_low, y_g, x_g]
    img_high = banco[idx_high, y_g, x_g]
    
    return w_low * img_low + w_high * img_high