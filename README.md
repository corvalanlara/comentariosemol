# Comentarios EMOL

Pequeño programa para generar un documento .csv con los comentarios publicados en las noticias de EMOL.

## Uso

Instalar usando `pip install comentariosemol`. Ejecutar en el terminal escribiendo `comentariosemol` seguido de la URL de la noticia cuyos comentarios se desean extraer. 

En forma opcional, tras la URL se puede añadir la ubicación (*path*) del archivo .csv por crear (dando el poder de elegir el nombre del archivo final). Si ésta última no se indica, el nombre del archivo que se creará será el *slug* de la URL de la noticia más la fecha y hora en que se generó la extracción.

También se puede seleccionar la cantidad de comentarios a extraer con la opción `-n` seguida del número límite de comentarios. El número corresponderá a los primeros n comentarios de la noticia.

Por último, en vez de ingresar una única URL es posible poner el *path* de un archivo .txt que contenga URLs separadas por coma.

## Configuración

En la primera ejecución el programa solicitará el *path* a una archivo ejecutable. Este archivo debe corresponder al navegador de preferencia instalado en el computador. Actualmente, este programa sólo trabaja con Chrome y Firefox.

* Si tienes Chrome, descarga el archivo [aquí](https://sites.google.com/a/chromium.org/chromedriver/downloads).
* Si prefieres Firefox, el archivo lo encontrarás [acá](https://github.com/mozilla/geckodriver/releases).

### Bugs

Si existieran errores en el programa se solicita comunicarlos al correo corvalanlara [arroba] protonmail [punto] com