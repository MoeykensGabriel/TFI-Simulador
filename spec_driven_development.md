# Desarrollo de Simulador

Nos encontramos desarrollando un simulador utilizando lo aprendido en la materia, como generacion de nros pseudoaleatorios, distribuciones de probabilidad, modelos y teorias de colas.

Para los modelos matematicos usamos las herramientas visuales con SW como Arena y DFD.

El objetivo es desarrollar una primera version simple pero funcional del simulador, todo de acuerdo a los datos establecios abajo de esta linea.

Utilizando Python, SimPy, Tkinter.

# Modelo Verbal 

Caso de estudio: Optimización del proceso de Clasificación 

Cliente: Jorge Santkovsky - Gerente de Logística y Operaciones de Scrap & Rezagos S.R.L.  

Socio Gerente de la empresa, quien tiene a su cargo la estrategia comercial, el cumplimiento de normativas ante ACUMAR y APrA, y la representación institucional ante cámaras del sector como CAMOCA. 

Intereses: **DESCRIPCIÓN DETALLADA DE INTERESES Y BENEFICIOS del cliente** 

Introducción y Contexto  

La empresa Scrap y Rezagos S.R.L., se dedica a la gestión integral de residuos electrónicos (RAEE) y la disposición segura de activos tecnológicos. Su operación principal se centra en la disposición final y reacondicionamiento de activos tecnológicos, específicamente teléfonos móviles y tabletas provenientes de recambios corporativos.   

La realidad operativa principal comienza en el Muelle de Entrada. La cual tiene una capacidad de procesamiento estimada de 1200 toneladas anuales de material tecnológico, donde 96 toneladas son de celulares y tablets. Se estima que la cantidad de lotes que arriban aquí son entre 3 y 7 lotes semanalmente El arribo de los lotes presenta una alta imprevisibilidad: las cargas llegan de forma irregular, con una cantidad preestablecida por lote de 450 ± 100 kg. Al ingresar a la planta, los lotes son desagregados en unidades individuales de dispositivos para su procesamiento en base a sus rangos de peso individuales. Esta aleatoriedad genera periodos de inactividad seguidos de picos de saturación que comprometen la capacidad de almacenamiento y procesamiento de la planta.  

Los pesos de los dispositivos se encuentran en un rango comprendido entre 140 a 300 gramos para celulares y de 300 a 700 gramos para Tablets.  

 

El Proceso de Clasificación  

El lote se compone aproximadamente en un 97% de celulares y un 3% de tablets. Además, alrededor del 30% son de tecnología moderna de los dispositivos. Las unidades ingresan y se trasladan a la Mesa de Clasificación, donde se disponen para trabajar actualmente 3 operarios técnicos. La tarea consiste en realizar un diagnóstico rápido y eficiente para derivar cada dispositivo a uno de los tres canales de salida:  

Tabla de probabilidad de canales 

Canal 

Probabilidad 

Acumulada 

Reventa 

0,30 

0,30 

Reciclaje 

0,40 

0,70 

Desecho 

0,30 

1 


Canal de Reventa: Para dispositivos funcionales que conservan valor comercial. Estos equipos deben someterse a un protocolo de borrado seguro de datos antes de ser reinsertados en el mercado para su venta. Estos son el 30 % de los dispositivos y los precios de reventa de los dispositivos comprenden entre $150.000 ARS y $350.000 ARS por unidad para celulares, y entre $250.000 ARS y $550.000 ARS por unidad para Tablets. 


Canal de Reciclaje: Para equipos con daños estructurales o software obsoleto. Se procede al desmantelamiento para la recuperación de elementos. La composicion de los dispositivos se divide en Plásticos, Metales y Vidrios. Estos son el 40 % de los dispositivos.  

Tabla de composición de dispositivos 

Material 

Composición 

Acumulada 

Precio 

Plásticos 

0,40 

0,40 

$1.450/kg 

Metales 

0,35 

0,75 

$45.100/kg 

Restantes (cerámica, vidrio, demás) 

0,25 

1 

$0/kg 

 

Canal de Desecho (Gris en el prototipo): Para componentes sin valor de recuperación o materiales peligrosos que requieren disposición final controlada. Estos son el 30 % de los dispositivos. 

 

Problemática: Variabilidad y Obsolescencia  

El Gerente de Logística y Operaciones (el cliente) debe asegurar que la planta procese las 8 toneladas mensuales promedio necesarias para alcanzar la meta anual sin generar cuellos de botella. Sin embargo, enfrenta tres problemas críticos:  

  

Incertidumbre en la Composición: La proporción de equipos funcionales frente a la chatarra solo se conoce al abrir los lotes, lo que dificulta la planificación del personal en el laboratorio de borrado seguro.  

Tecnología Moderna: Los dispositivos de última generación requieren protocolos de tratamiento que las normas actuales de la empresa no contemplan con eficiencia, triplicando el tiempo de procesamiento de datos en comparación con equipos más antiguos. 

Margen de Error: Se ha detectado una probabilidad de error del 3% en la clasificación manual, donde equipos aptos para reventa terminan siendo destruidos, afectando la rentabilidad operativa.  

 
Para optimizar el flujo y mejorar la rentabilidad, el Gerente debe evaluar las siguientes situaciones condicionales:  

 
Alternativa A: Gestión de la Capacidad del Muelle:  

SI (IF) el tiempo medio de espera de los dispositivos supera los 3 minutos Y la ocupación del depósito de recepción es mayor al 90%, ENTONCES la solución para el cliente es autorizar la apertura de una cuarta estación de clasificación temporal; CASO CONTRARIO (ELSE) se mantiene la operación con el equipo de 3 técnicos para minimizar costos fijos.  

Alternativa B: Transición Tecnológica:  

SI (IF) el porcentaje de dispositivos de nueva generación (Modernos) recibidos en el mes supera el 35% del total Y el cuello de botella se traslada sistemáticamente al área de borrado seguro, ENTONCES el cliente debe invertir en la actualización de las normas y software de tratamiento; CASO CONTRARIO (ELSE) se mantiene el protocolo actual priorizando la rapidez en el flujo de reciclaje básico.  

Alternativa C: Mejora en la Precisión de Clasificación:  

SI (IF) el costo de los equipos funcionales destruidos por error de clasificación supera el margen de rentabilidad previsto (Margen de Rentabilidad Previsto en un 15% sobre los ingresos brutos proyectados de la planta), ENTONCES la solución es implementar herramientas de diagnóstico automatizado para asistir a los operarios; CASO CONTRARIO (ELSE) se mantiene el proceso manual actual reforzando la capacitación del personal.  

Alternativa D: Activación de Puesto de Re-inspección:  

SI (IF) la Tasa Acumulada de Pérdida Económica por desecho erróneo de equipos funcionales supera el costo equivalente a un salario técnico durante el mes simulado ($1.100.000/operario), ENTONCES la solución operativa es agregar temporalmente un técnico para realizar una re-inspección rápida (auditoría) exclusivamente en la cola del canal de desecho antes de la inutilización física; CASO CONTRARIO (ELSE) se confía plenamente en el primer filtrado de la mesa de clasificación y todo el personal se concentra en agilizar el desmantelamiento manual básico. 

 
# Bloques y Módulos del Modelo 

Create (Llegada de Lotes): Define el proceso de arribos del sistema. Configura la llegada aleatoria de las cargas con la función de distribución uniforme UNIF(0.6, 1.4) por dia. Genera las entidades "lote padre" en el muelle de entrada. 

Separate (Desagregar Lote en Unidades): Aplica la lógica de Duplicate Original para realizar un escalado de unidades y evitar saturar el límite físico de 150 entidades simultáneas de la versión Student. Divide el lote padre en un valor fijo de 50 duplicados para el flujo operativo y destruye el lote original. 

Assign (Asignar Atributos Iniciales): Define las propiedades y variables de estado iniciales de cada entidad usando funciones estadísticas discretas acumuladas (DISC). Específicamente asigna: 

Tipo de dispositivo: TipoDispositivo = DISC(0.72, 1, 1.0, 2) (donde 1 es Celular y 2 es Tablet). 

Nivel tecnológico: Tecnologia = DISC(0.70, 1, 1.0, 2) (donde 1 es Antiguo y 2 es Moderno). 

Gráfico en pantalla: Atributo Entity Picture vinculado a los íconos personalizados de celulares y tablets. 

Decide (Rombos de bifurcación lógica): Actúan como los controladores de flujo condicional del modelo. 

Usan la variante 2-way by Condition para comprobar atributos matemáticos (por ejemplo, validar si TipoDispositivo == 1 para asignar sus respectivos rangos de peso con UNIF). 

Usan la variante N-way by Chance para el desvío probabilístico final de los canales de salida según los porcentajes: 30% para Reventa, 40% para Reciclaje y 30% para Desecho. 

Process (Mesa de Clasificación): Modela el núcleo de atención del sistema como un nodo de servicio de servidores en paralelo (M/M/3). Utiliza la lógica Seize Delay Release asociada al recurso Operario Tecnico con una capacidad global de 3. Si los 3 Operarios están ocupados, las entidades forman una fila automática bajo disciplina FIFO, permitiendo medir los indicadores de Theory of Queues: longitud promedio de la fila (L_q) y tiempo de espera (W_q). 

Process (Borrado Seguro Moderno y Borrado Seguro Antiguo): Representan subprocesos independientes en el canal de reventa. Permiten modelar la penalización de tiempo del laboratorio mediante expresiones lógicas. El borrado moderno se configuró con la función de retraso multiplicada por tres: UNIF(10, 15) * 3. 

Process (Puesto de Re-inspección): Bloque operativo intermitente que representa la Alternativa D del problema. Utiliza la acción Seize Delay Release para tomar de forma dinámica a uno de los operarios de la mesa de entrada principal y procesar el flujo desviado. 

Dispose (Sumideros del sistema): Son los puntos de salida definitivos.  Las entidades finalizan el recorrido y consolidan la variable interna Number Out para obtener el volumen de producción total del período. 

Variables e Indicadores Globales 

Variable (PerdidaAcumulada): Variable global dada de alta en la planilla de datos (Data Definition) para registrar el impacto financiero del desecho erróneo del 3%. Cada vez que una entidad pasa por el bloque de error, ejecuta la ecuación recursiva en memoria: 

PerdidaAcumulada = PerdidaAcumulada + 250000$ 

Esta variable es monitoreada continuamente por el módulo Decide de la Alternativa D mediante la condición: 

PerdidaAcumulada > 1100000$ 

Al volverse verdadera, el sistema activa automáticamente las compuertas físicas para desviar los dispositivos hacia el puesto de Re inspección. 

Interfaz del Simulador 

Descripción: 

Parámetros (Columna Izquierda) 

Sección destinada a la configuración del modelo por parte del usuario. Permite modificar las variables operativas y los parámetros de las distribuciones de probabilidad: 

Cantidad de lotes por semana (valor inferior y superior) 

Tamaño de Lote (media y desviación) 

Precios de venta de tablets (valor inferior y superior) 

Precios de venta de celulares (valor inferior y superior) 

Margen de rentabilidad 

Cantidad de operarios 

Salario técnico  

Botón para iniciar la simulación 

 

Flujo de Dispositivos (Columna Central) 

Representación visual y dinámica que simplifica el recorrido de los materiales a lo largo del proceso, informando en tiempo real: 

Volumen total de dispositivos que entran a la planta. 

Cantidad de operarios asignados al proceso de clasificación. 

Indicadores con el conteo a los dispositivos asignados a cada estado tras la clasificación. 

 

Resultados (Columna Derecha):  salidas para evaluar distintos escenarios y facilitar la toma de decisiones estratégicas a través de recomendaciones clave: 

Gestión de la capacidad del muelle. 

Transición tecnológica de la planta. 

Mejora en la precisión de clasificación. 

Activación de puesto de re-inspección.  

 

	 

 

Modelo matemático: 

• Realizar el modelo matemático -> Diagrama de flujo. Como referencia tengan en cuenta el  

tamaño de los diagramas de flujo de los ejercicios propuestos. (Tamaño mínimo  

aproximado).  

La nota del trabajo final integrador dependerá, entre otros factores, del tamaño del diagrama. 

La implementación posterior y el diagrama tienen que ser coherentes. Este punto será  chequeado.  

• Colocar una imagen que refleje algún aspecto de su caso de estudio (Modelo icónico) 

 

Respecto a Teoría de Colas: 

Incorporamos Teoría de Colas en su Trabajo Final Integrador. Debe tener coherencia y reflejar la realidad.  

Para la implementación de este contenido, se solicita: 

a) Redactar el problema (o un aspecto del mismo) usando terminología de “Teoría de  

Colas”. Es un enunciado “extra” que será puesto por separado del enunciado de  

“Distribuciones de Probabilidad”, siempre dentro de la temática elegida. Deberán usar  

de manera obligatoria los módulos mencionados en clase y todos los que deseen  

agregar. 

b) Implementar ese contenido en el Software Arena u otro similar. 

c) Hacer capturas de pantallas de lo realizado (Mínimo dos capturas diferentes). 

d) Explicar qué hizo para lograr el objetivo: ¿qué módulos usó?  

e) Se les pedirá que suban el archivo de Arena (Archivo *.doe). 

En una empresa dedicada al procesamiento y clasificación de dispositivos electrónicos reciclados, los productos llegan al muelle de entrada para ser inspeccionados y clasificados antes de continuar con el proceso logístico. 

La llegada de dispositivos se produce en lotes semanales, donde por cada lote la empresa recibe aproximadamente entre 2550 y 20811 dispositivos electrónicos por semana. 

Una vez descargados en el muelle, los dispositivos ingresan a un sistema de inspección y clasificación compuesto por una única mesa de clasificación atendida por 3 operarios en paralelo. Cada operario inspecciona y clasifica los dispositivos de manera individual. 

El tiempo de servicio por dispositivo varía entre 1 a 3 minutos, dependiendo del estado y complejidad del equipo recibido. Cuando todos los operarios se encuentran ocupados, los dispositivos deben esperar en una cola hasta que uno de los servidores quede disponible. 

La empresa desea analizar el comportamiento del sistema de colas para determinar: 

El tiempo promedio de espera de los dispositivos en cola.  

La longitud promedio de la cola de dispositivos pendientes de clasificación.  

El nivel de utilización de los operarios.  

La probabilidad de congestión en la mesa de clasificación.  

La capacidad del sistema para responder ante incrementos en la llegada de lotes semanales. 





# Tiempo y forma de Simulación: 4 semanas (semana a semana) 




# DICCIONARIO DEL MODELO MATEMATICO

_Detalle de variables utilizadas en nuestro modelo._

---

## Modelo Matemático

**INICIO**
- _S_: Semanas.

- _L_: Lote.

- _PL_: Peso del lote.

- _SP_: Suma de pesos de Dispositivos.

- _C_: Celulares.

- _T_: Tablets.

- _TTM_: Tablets Total Moderno.

- _CTM_: Celular Total Moderno.

- _PD_: Peso Dispositivo.


**CLASIFICACIÓN DISPOSITIVO 1**
- _C_: Celulares.

- _CMC_: Celulares Mal Clasificados.

- _CRV_: Celulares para Reventa.

- _CRC_: Celulares para Reciclaje.

- _CD_: Celulares Desecho.


**CLASIFICACIÓN DISPOSITIVO 2**

- _T_: Tablets.

- _TMC_: Tablets Mal Clasificados.

- _TRV_: Tablets Reventa.

- _TRC_: Tablets para Reciclaje.

- _TD_: Tablets Desecho.


**PRECIO REVENTA 1**

- _CRV_: Celulares para Reventa.

- _VCI_: Valor de Precio Celular Inferior.

- _VCS_: Valor de Precio Celular Superior.

- _TC_: Total de precio de celulares.


**PRECIO REVENTA 2**

- _TRV_: Tablets para Reventa.

- _VTI_: Valor de Precio Tablets Inferior.

- _VTS_: Valor de Precio Tablets Superior.

- _TT_: Total de precio Tablets.


**CALCULO MATERIALES 1**

- _CRC_: Celulares para Reciclaje.

- _LPIC_: Limite de Peso Inferior de Celulares.

- _LPSC_: Limite de Peso Superior de Celulares.

- _CPC_: Cantidad de Plasticos del Celular.

- _CMC_: Cantidad de Metal del Celular.

- _CVC_: Cantidad de Vidrio del Celular.


**CALCULO MATERIALES 2**

- _TRC_: Tablets para Reciclaje.

- _LPIT_: Limite de Peso Inferior de Tablets.

- _LPST_: Limite de Peso Superior de Tablets.

- _CPT_: Cantidad de Plasticos de Tablet.

- _CMT_: Cantidad de Metal de Tablet.

- _CVT_: Cantidad de Vidrio de Tablet.


**FINAL**

- _GTR_: Ganancia Total de Reventa.

- _TC_: Total de peso de Celulares.

- _TT_: Total de peso de Tablets.

- _PT_: Plastico peso Total (Tablets + Celulares).

- _CPC_: Cantidad de Plasticos del Celular.

- _CPT_: Cantidad de Plasticos de Tablet.

- _MT_: Metal Total (Tablets + Celulares).

- _CMC_: Cantidad de Metal del Celular.

- _CMT_: Cantidad de Metal de Tablet.

- _VT_: Vidrio Total (Tablets + Celulares).

- _CVC_: Cantidad de Vidrio del Celular.

- _CVT_: Cantidad de Vidrio de Tablet.

- _GTM_: Ganancia Total de Materiales.

- _GTN_: Ganancia Total Neta.

- _MR_: Margen de Rentabilidad.

- _CDM_: Cantidad de Dispositivos Modernos.

- _CTM_: Celulares Total Moderno.

- _TTM_: Tablets Total Moderno.

- _T_: Tablets.

- _C_: Celulares.

- _DMC_: Dispositivos Mal Clasificados.

- _CMC_: Celulares Mal Clasificados.

- _TMC_: Tablets Mal Clasificados.


**PRECIO REVENTA 3**

- _DMC_: Dispositivo Mal Clasificado.

- _VDCI_: Valor de Peso Dispositivo Inferior.

- _VDCS_: Valor de Peso Dispositivo Superior.

- _TCDMC_: Total de Cantidad de Dispositivos Mal Clasificados.


**ESCENARIOS**

- _GTN_: Ganacia total neta.

- _MR_: Margen de Rentabilidad.

- _TD_: Total Dispositivos.

- _CDM_: Cantidad de Dispositivos Modernos.

- _TCDMC_: Total de Cantidad de Dispositivos Mal Clasificados.

- _PTT_: Promedio Total de Tiempo.

- _ST_: Suma de Tiempos.

- _CT_: Clasifición Tiempo.


**CLASIFICACIÓN DISPOSITIVO - GENERAL**

- _D_: Dispositivos.

- _DMC_: Dispositivos Mal Clasificados.

- _DRV_: Dispositivos Reventa.

- _DRC_: Dispositivos para Reciclaje.

- _DD_: Dispositivos Desecho.


**PRECIO REVENTA - GENERAL**

- _DRV_: Dispositivos Reventa.

- _VLI_: Valor de precio Limite Inferior.*

- _VLS_: Valor de precio Limite Superior.*

- _PT_: Precio Total.

- _P_: Precio.


**CALCULO DE MATERIALES - GENERAL**

- _DRC_: Dispositivos Reciclaje.

- _LPI_: Limite Peso Inferior.

- _LPS_: Limite Peso Superior.

- _CP_: Cantidad Plastico.

- _CM_: Cantidad Metal.

- _CV_: Cantidad Vidrio.

- _PD_: Precio Dispositivo.


## Descripción

- Comenzamos con una simulación semanal de 4 semanas, ingresan los lotes (dist. uniforme) y por cada lote segun su peso (dist. normal), evaluamos la cantidad de celulares y tablets en un late sabiendo que entre dispositivos moviles (tablets y celulares) los celulares representan el 97% (dist. binomial).
- Los dispositivos modernos

