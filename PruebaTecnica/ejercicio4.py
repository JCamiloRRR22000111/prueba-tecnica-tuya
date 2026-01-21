import base64
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict

class ImageConverter:

    @staticmethod #Función estatica, no es necesario crear un objeto
    def image_to_base64(image_path: Path) -> str:
        try:
            with open(image_path, "rb") as f: #Se abre el archivo en modo binario
                
                #lee los bytes de la imagen y los convierte a base64
                #de base64 los convierte a cadena de texto para poder ponerlos en el html
                encoded = base64.b64encode(f.read()).decode("utf-8") 
            # Incrusta la cadena base64 al html
            return f"data:image/{image_path.suffix[1:]};base64,{encoded}"
        except Exception:
            return ""  # Devuelve vacío si falla la conversión


class HTMLImageParser(HTMLParser):
    # Parser para extraer todas las imágenes de un HTML.

    #Constructor de la clase
    def __init__(self):
        super().__init__() # llama al constructor de HTMLParser para que se inicialice correctamente
        self.images: List[str] = [] #Crea una lista vacía donde se van a guardar las rutas de todas las imagenes
        
    #Cada que HTMLParser encuentra una etiqueta de apertura se llama a este metodo
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img": #Verifica si la etiqueta de la imagen es de tipo img
            
            #attrs es una lista de tuplas que representan las etiquetas de la imagen
            # Se convierte dicha lista de tuplas en un diccionario
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src", "") #Se busca el atributo src que contiene el nombre de la imagen y si no tiene se busca "" por defecto
            if src: #si src no esta vacio
                self.images.append(src) #se agrega a la lista de imagenes

def gather_html_files(paths: List[Path]) -> List[Path]:
    # Esta funcion recibe una lista de archivos o directorios y devuelve todos los archivos HTML encontrados.
    
    html_files = []

    for path in paths: #Crea un bucle que recorre cada una de las direcciones que tiene paths
        #Verifica si la ruta corresponde a un archivo y dicho archivo tiene extensión HTML
        if path.is_file() and path.suffix.lower() == ".html":
            # Si es un archivo HTML, se agrega directamente a la lista
            html_files.append(path)
        elif path.is_dir(): #El el caso de que la ruta no corresponda a un archivo
            # Si es un directorio, recorremos todos los archivos dentro, incluyendo subdirectorios
            for file_path in path.rglob("*.html"):  
                html_files.append(file_path) #agrega a la lista los archivos html que encuentre

    return html_files #Retorna el valor de la lista


def process_html_files(html_files: List[Path], output_dir: Path) -> Dict[str, Dict[str, List[str]]]:
   
    results = {"success": {}, "fail": {}}

    # Se verifica que existe la carpeta de salida
    output_dir.mkdir(exist_ok=True)
    
    #Se realiza un bucle for que itera cada una de las direcciones encontradas anteriormente
    for html_file in html_files:
        
        parser = HTMLImageParser() #Se crea un objeto de la clase HTMLImageParser
        html_content = html_file.read_text(encoding="utf-8") # Se abre y se lee todo el contenido del documento que se está analizando
        parser.feed(html_content) #feed() es un metodo de la clase HTMLParser que recorre y analiza todo el html

        modified_html = html_content  # se crea la copia que se va a modificar
        success_imgs = []
        fail_imgs = []
        
        #Bucle que recorre todas las imagenes que el objeto parser encontró
        for img_src in parser.images:
            
            # sirve para obtener la ruta relativa de la imagen
            # En este caso unifica la ruta donde esta el archivo html y la ruta donde se encuentra la imagen
            img_path = (html_file.parent / img_src).resolve()
            base64_str = ImageConverter.image_to_base64(img_path)#se llama a la clase imageconverter y se le pasa la ruta de la imagen
            if base64_str:
                # Reemplazamos la ruta de la imagen por la cadena Base64
                modified_html = modified_html.replace(img_src, base64_str)
                success_imgs.append(img_src)
            else:
                fail_imgs.append(img_src)

        # se guarda el archivo nuevo sin sobrescribir el original
        new_file = output_dir / f"{html_file.stem}_base64.html"
        new_file.write_text(modified_html, encoding="utf-8")

        # se guardan los resultados
        if success_imgs:
            results["success"][str(html_file)] = success_imgs
        if fail_imgs:
            results["fail"][str(html_file)] = fail_imgs

    return results


# Ruta de la carpeta donde debe de encontrar los archivos html
paths = [
    Path("C:/Users/jonat/Documents/PruebaTecnica/paginas"), # Directorio completo
    Path("C:/Users/jonat/Documents/PruebaTecnica/pagina3.html") #Archivo en concreto
]

# se llama a la funcion
html_files = gather_html_files(paths)
output_directory = Path("C:/Users/jonat/Documents/PruebaTecnica/htmlbase64")  # carpeta para los HTML con Base64

results = process_html_files(html_files, output_directory)

print("Resultados del procesamiento de imágenes:")
print(results)
