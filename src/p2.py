import numpy as np
import scipy.ndimage
import scipy.signal

# Función para calcular el error cuadrático medio (RMSE) entre la imagen de referencia y la imagen estimada
def rmse(ref, est):
    return np.sqrt(np.mean((ref - est) ** 2))

# calcula los grad discr hacia 4 vecinos (N,E,S,W)
# derivadas nulas en bordes
def gradientes_4_direc(u):
    dN = np.pad(u[:-1, :] - u[1:, :], ((1, 0), (0, 0)), mode='constant')
    dS = np.pad(u[1:, :] - u[:-1, :], ((0, 1), (0, 0)), mode='constant')
    dE = np.pad(u[:, 1:] - u[:, :-1], ((0, 0), (0, 1)), mode='constant')
    dW = np.pad(u[:, :-1] - u[:, 1:], ((0, 0), (1, 0)), mode='constant')
    return dN, dS, dE, dW

# calcula la magnitud del gradiente al cuadrado a partir de los gradientes discretos
def magnitud_gradiente_cuadrado(dN, dS, dE, dW):
    dx = (dE - dW) / 2.0
    dy = (dS - dN) / 2.0
    return dx**2 + dy**2

# laplaciano (ayudantia)
def laplaciano_discreto(u):
    kernel = np.array([
        [0.0, 1.0, 0.0],
        [1.0, -4.0, 1.0],
        [0.0, 1.0, 0.0]
    ], dtype=np.float64)
    return scipy.signal.convolve2d(u, kernel, mode='same', boundary='symm')

# Coef VT = epsilon / sqrt(|grad u|^2 + epsilon^2)
# normalizado para acotar c_max <= 1.0
def coef_TV(u, grad_sq, lap, dN, dS, dE, dW, eps=0.01):
    c_map = eps / np.sqrt(grad_sq + eps**2)
    # Eval de coef en los medios pixeles
    cN = np.pad((c_map[:-1, :] + c_map[1:, :]) / 2.0,
                ((1, 0), (0, 0)), mode='edge')
    cS = np.pad((c_map[1:, :] + c_map[:-1, :]) / 2.0,
                ((0, 1), (0, 0)), mode='edge')
    cE = np.pad((c_map[:, 1:] + c_map[:, :-1]) / 2.0,
                ((0, 0), (0, 1)), mode='edge')
    cW = np.pad((c_map[:, :-1] + c_map[:, 1:]) / 2.0,
                ((0, 0), (1, 0)), mode='edge')
    return cN, cS, cE, cW, c_map


# Propuesta 1: Función Racional basada en Gradiente
# c1 = 1 / (1 + (|grad u| / K)^alpha)
def coef_gradiente(u, grad_sq, lap, dN, dS, dE, dW, K=0.05, alpha=2.0):
    grad_mag = np.sqrt(grad_sq)
    c_map = 1.0 / (1.0 + (grad_mag / K)**alpha)
    
    cN = np.pad((c_map[:-1, :] + c_map[1:, :]) / 2.0, ((1, 0), (0, 0)), mode='edge')
    cS = np.pad((c_map[1:, :] + c_map[:-1, :]) / 2.0, ((0, 1), (0, 0)), mode='edge')
    cE = np.pad((c_map[:, 1:] + c_map[:, :-1]) / 2.0, ((0, 0), (0, 1)), mode='edge')
    cW = np.pad((c_map[:, :-1] + c_map[:, 1:]) / 2.0, ((0, 0), (1, 0)), mode='edge')
    return cN, cS, cE, cW, c_map

# Propuesta 2: Función Exponencial basada en Laplaciano y Gradiente Estabilizado
# E = |grad u| + gamma * |grad^2 u_suave|
# c2 = exp( - (E / K_comb)^2 )
def coef_laplaciano(u, grad_sq, lap, dN, dS, dE, dW, K_g=0.05, K_l=0.10, gamma=0.5, sigma_pre=0.5):

    if sigma_pre > 0:
        u_suave = scipy.ndimage.gaussian_filter(u, sigma=sigma_pre)
        lap_estabilizado = laplaciano_discreto(u_suave)
    else:
        lap_estabilizado = lap
        
    grad_mag = np.sqrt(grad_sq)
    indicador_E = grad_mag + gamma * np.abs(lap_estabilizado)
    K_comb = K_g + gamma * K_l
    
    c_map = np.exp(- (indicador_E / K_comb)**2)
    
    cN = np.pad((c_map[:-1, :] + c_map[1:, :]) / 2.0, ((1, 0), (0, 0)), mode='edge')
    cS = np.pad((c_map[1:, :] + c_map[:-1, :]) / 2.0, ((0, 1), (0, 0)), mode='edge')
    cE = np.pad((c_map[:, 1:] + c_map[:, :-1]) / 2.0, ((0, 0), (0, 1)), mode='edge')
    cW = np.pad((c_map[:, :-1] + c_map[:, 1:]) / 2.0, ((0, 0), (1, 0)), mode='edge')
    return cN, cS, cE, cW, c_map

# Función principal de difusión anisotrópica
# u^{k+1} = u^k + dt * \sum_dir (c_dir * grad dir u)
def difusion_anisotropica(u0, func_coef, n_iter=80, dt=0.20, **kwargs):

    u = u0.copy()
    
    for k in range(n_iter):
        dN, dS, dE, dW = gradientes_4_direc(u)
        grad_sq = magnitud_gradiente_cuadrado(dN, dS, dE, dW)
        lap = laplaciano_discreto(u)
        
        cN, cS, cE, cW, c_map = func_coef(u, grad_sq, lap, dN, dS, dE, dW, **kwargs)
        u = u + dt * (cN * dN + cS * dS + cE * dE + cW * dW)
        
    return u, c_map