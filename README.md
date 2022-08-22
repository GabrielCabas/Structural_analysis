## Instrucciones

  -  Clonar repositorio.
  
  -  Extraer data.zip en la carpeta principal del proyecto.

  -  Comentar línea 96 para correr el script con la totalidad de datos. 

    pip3 install -r requirements.txt
    cd Predict_Property/source_code/
    make
    cd ../../
    python3 structural_characterization.py

El script es secuencial, no está paralelizado. 

Es posible dividir los .csv en mas partes para distribuir los cálculos.
