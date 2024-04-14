import cv2
import numpy as np

class ComprobarCirculoAzul:
    # Definir h_bajo y h_alto como atributos de clase
    h_bajo = 100
    h_alto = 120
    def __init__(self, nombre_imagen):
        nombre_mascara = 'mascaraCirculoAzul.jpg'
        self.imgC = cv2.imread(nombre_imagen)
        self.mascaradeprueba = self.generar_mascara(nombre_mascara)
        self.rectangles_filtrados = []
        self.detectar_y_filtrar_rectangulos()

    def generar_mascara(self, nombre_mascara):
        imagenMascara = cv2.imread(nombre_mascara, cv2.IMREAD_GRAYSCALE)
        mascara_reescalada = cv2.resize(imagenMascara, (25, 25))
        resultado = self.procesar_imagen(mascara_reescalada)
        return resultado

    def procesar_imagen(self, nombre_imagen):
        if nombre_imagen is not None and len(nombre_imagen.shape) == 2:
            matriz = np.array(nombre_imagen)
            matriz_resultante = np.where(matriz == 255, 1, 0)
            matriz_resultante = matriz_resultante.reshape(25, 25)
            return matriz_resultante
        else:
            return None

    def detectar_y_filtrar_rectangulos(self):
        imgBN = cv2.cvtColor(self.imgC, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create(delta=1, max_variation=0.15, min_area=100, max_area=15000)
        polygons = mser.detectRegions(imgBN)
        self.rectangles_filtrados = [cv2.boundingRect(polygon) for polygon in polygons[0] if
                                     self.filtrar_rectangulo(cv2.boundingRect(polygon))]

    def filtrar_rectangulo(self, rect):
        x, y, w, h = rect
        base = np.linalg.norm(np.array((x, y)) - np.array((x + w, y)))
        altura = np.linalg.norm(np.array((x + w, y)) - np.array((x + w, y + h)))
        relacion = base / altura
        return 0.90 <= relacion <= 1.10

    def recortar_y_mostrar_secciones_hsv(self):
        coordenadas_cumplen_condicion = []
        medias_vistas = set()

        # Verificar si hay rectángulos filtrados antes de proceder
        if not self.rectangles_filtrados:
            print("No se encontraron rectángulos filtrados.")
            return coordenadas_cumplen_condicion

        for i, rect in enumerate(self.rectangles_filtrados):
            x, y, w, h = rect
            seccion_recortada = self.imgC[y:y + h, x:x + w]
            seccion_hsv = cv2.cvtColor(seccion_recortada, cv2.COLOR_BGR2HSV)
            componente_h = seccion_hsv[:, :, 0]
            mascara_h = cv2.inRange(componente_h, self.h_bajo, self.h_alto)  # Usar h_bajo y h_alto de la clase
            seccion_reescalada = cv2.resize(mascara_h, (25, 25))
            resultadodematriz = self.procesar_imagen(seccion_reescalada)
            cantidad_de_unosP = np.count_nonzero(resultadodematriz == 1)
            cantidad_de_unos_Mascara = np.count_nonzero(self.mascaradeprueba == 1)
            resultado = resultadodematriz * self.mascaradeprueba
            aux1 = 1 - resultadodematriz
            aux2 = 1 - self.mascaradeprueba
            resultado2 = aux1 * aux2
            cantidad_de_unos = np.count_nonzero(resultado == 1)
            cantidad_de_unos2 = np.count_nonzero(resultado2 == 1)
            cantidad_de_unos_MascaraInvertida = np.count_nonzero(aux2 == 1)
            unos_de_la_primera_multiplicacion = cantidad_de_unos_Mascara - cantidad_de_unos
            unos_de_la_segunda_multiplicacion = cantidad_de_unos_MascaraInvertida - cantidad_de_unos2
            media_Unos = (unos_de_la_primera_multiplicacion + unos_de_la_segunda_multiplicacion) / 2
            if cantidad_de_unos > 5 and cantidad_de_unos2 < 200 and media_Unos not in medias_vistas and cantidad_de_unosP > 90 and cantidad_de_unos > 48:
                coordenadas_cumplen_condicion.append((x, y, x + w, y + h, media_Unos))
                medias_vistas.add(media_Unos)

        return coordenadas_cumplen_condicion