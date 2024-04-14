import argparse
import cv2

#if __name__ == "__main__":

    #parser = argparse.ArgumentParser(
        #description=('Crea y ejecuta un detector sobre las imágenes de test')
    #parser.add_argument(
        #'--detector', type=str, nargs="?", default="", help='Nombre del detector a ejecutar')
    #parser.add_argument(
        #'--train_path', default="", help='Carpeta con las imágenes de entrenamiento')
    #parser.add_argument(
        #'--test_path', default="", help='Carpeta con las imágenes de test')

    #args = parser.parse_args()

    # Cargar los datos de entrenamiento sin se necesita
    # print("Cargando datos de entrenamiento desde " + args.train_path)

    # Create the detector
    #print("Creando el detector " + args.detector)

    # Cargar los datos de test y ejecutar el detector en esas imágenes
    #print("Probando el detector " + args.detector + " en " + args.test_path)

    # Guardar resultados en el fichero resultado.txt

    # Guardar resultados en el fichero resultado_por_tipo.txt

from comprobarCirculoRojo import ComprobarCirculoRojo
from comprobarCirculoAzul import ComprobarCirculoAzul

def main():
    nombre_imagen = 'test_alumnos\\00715.ppm'
    nombre_imagen2 = 'test_alumnos\\00715.ppm'
    circulo_rojo_checker = ComprobarCirculoRojo(nombre_imagen)

    coordenadas_cumplen_condicion = circulo_rojo_checker.recortar_y_mostrar_secciones_hsv()

    circulo_azul_checker2 = ComprobarCirculoAzul(nombre_imagen)

    coordenadas_cumplen_condicion2 = circulo_azul_checker2.recortar_y_mostrar_secciones_hsv()

    coordenadas_totales = coordenadas_cumplen_condicion + coordenadas_cumplen_condicion2

    # Hacer algo con coordenadas_cumplen_condicion, por ejemplo imprimir:
    print("Coordenadas de rectángulos que cumplen la condición:")
    for coords in coordenadas_totales:
        print(coords)
    imagen_original = cv2.imread(nombre_imagen)

    for coords in coordenadas_totales:
        x1, y1, x2, y2, _ = coords
        cv2.rectangle(imagen_original, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Imagen original con rectángulos", imagen_original)
    cv2.waitKey(10)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()




