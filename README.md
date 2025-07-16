Implementación de una estrategia de trading utilizando el framework Backtrader y datos históricos de acciones (AAPL, GOOG, MSFT, TSLA) correspondientes al año 2021.

El proyecto incluye tres estrategias basadas en medias móviles simples (SMA):

- Dos estrategias de cruce del precio de cierre con una SMA (con periodos de 10 y 30).

- Una estrategia basada en el cruce entre dos medias móviles (Golden Cross).

Cada estrategia gestiona de forma independiente sus propias posiciones por activo, registrando la lógica utilizada para cada compra y asegurando que las ventas solo se realicen mediante la misma estrategia que originó la entrada.

Durante la simulación, se destina el 10% del valor total del portafolio a cada nueva compra, siempre que haya liquidez suficiente.

Todas las operaciones y la evolución del capital se registran en un archivo CSV (`logs.csv`) ubicado en la carpeta `output/`, que se generará al ejecutar el proyecto.