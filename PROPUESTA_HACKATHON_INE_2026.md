# Propuesta técnica — Hackathon INE 2026
## Modelo de riesgo de abstención y simulación de escenarios territoriales

---

## 1. Contexto del reto

**Objetivo:** analizar información histórica y características de los territorios para identificar dónde podría disminuir la participación ciudadana, plantear escenarios y proponer acciones preventivas.

**Entregables solicitados:**

1. Construir un modelo simple de riesgo de abstención a partir de tendencias históricas de participación y variables sociodemográficas.
2. Simular al menos dos escenarios: sin intervención y con una intervención hipotética.
3. Traducir los resultados a un esquema de riesgo territorial fácil de interpretar.
4. Formular recomendaciones preventivas a partir de los escenarios.

---

## 2. ¿Se puede usar IA para las predicciones?

**Sí.** El problema es de aprendizaje supervisado sobre datos tabulares agregados por territorio (sección electoral, distrito o municipio). Puede plantearse de dos formas:

- **Regresión:** predecir el porcentaje de participación esperado.
- **Clasificación:** asignar un nivel de riesgo (alto / medio / bajo).

Se recomienda entrenar el modelo como regresión y derivar la clasificación a partir de umbrales, ya que así se conserva el valor continuo para las simulaciones.

---

## 3. Fuentes de datos

| Fuente | Datos | Uso |
|---|---|---|
| **INE – Sistema de Consulta de la Estadística de las Elecciones** | Participación por sección electoral (2012, 2015, 2018, 2021, 2024), lista nominal, votos nulos, tipo de elección | Variable objetivo y tendencia histórica |
| **INE – Cartografía electoral** | Shapefiles de secciones, distritos y municipios | Mapa de riesgo territorial |
| **INEGI – Censo de Población y Vivienda 2020** | Población por edad, escolaridad, ocupación, vivienda, migración, acceso a internet | Variables sociodemográficas |
| **CONAPO** | Índice de marginación por localidad/municipio | Variable de contexto socioeconómico |
| **INE – Ubicación de casillas** | Número y ubicación de casillas por sección | Accesibilidad al voto |

> Todos los datos son abiertos y agregados; no se utiliza información personal.

---

## 4. Variables propuestas

**Variable objetivo (y):**
- Porcentaje de participación en la elección más reciente (o cambio respecto a la anterior).

**Variables predictoras (X):**

| Grupo | Variable |
|---|---|
| Tendencia histórica | Participación en las últimas 3–4 elecciones; pendiente de la tendencia; volatilidad |
| Tipo de elección | Presidencial / intermedia / local concurrente |
| Demografía | % población 18–29 años; % mayores de 60; tamaño de lista nominal |
| Educación | Grado promedio de escolaridad; % sin secundaria terminada |
| Contexto socioeconómico | Índice de marginación; % ocupados; % viviendas con internet |
| Territorio | Ruralidad (urbano / mixto / rural); densidad poblacional |
| Accesibilidad | Casillas por cada 1 000 electores; distancia promedio a casilla |
| Comportamiento electoral | % votos nulos históricos; competitividad (margen entre primer y segundo lugar) |
| Movilidad | % población migrante o con residencia en otro estado 5 años antes |

---

## 5. Modelos recomendados

### 5.1 Modelo base (explicabilidad)

| Modelo | Justificación |
|---|---|
| **Regresión lineal / Ridge** | Los coeficientes indican directamente cuánto empuja cada variable la abstención. Sirve como línea base y para justificar hallazgos ante el jurado. |
| **Regresión logística** | Alternativa si se plantea como clasificación binaria (riesgo alto vs. resto). |

### 5.2 Modelo principal (desempeño)

| Modelo | Justificación |
|---|---|
| **Gradient Boosting (LightGBM / XGBoost / CatBoost)** | Mejor desempeño en datos tabulares. Captura no linealidades e interacciones (ej. juventud × ruralidad). Entrenamiento rápido, bajo costo computacional. |
| **Random Forest** | Alternativa robusta con menos ajuste de hiperparámetros. Buen punto de comparación. |

### 5.3 Explicabilidad

| Herramienta | Justificación |
|---|---|
| **SHAP (SHapley Additive exPlanations)** | Explica la predicción de *cada territorio*: qué variables elevan o reducen su riesgo. Es la base para recomendaciones focalizadas y diferenciadas por zona. |

### 5.4 Qué NO se recomienda

- **Redes neuronales profundas:** con ~68 000 secciones y pocas elecciones históricas no aportan mejora y sacrifican interpretabilidad.
- **LLMs para predecir:** no son adecuados para regresión numérica sobre datos tabulares. Su lugar es la redacción de recomendaciones (ver sección 8).

### 5.5 Validación

- **Validación temporal:** entrenar con elecciones hasta 2018/2021 y evaluar prediciendo 2024. Nunca usar división aleatoria, porque filtra información del futuro.
- **Métricas:** MAE y RMSE para regresión; precisión, recall y F1 para la clasificación de riesgo alto. Se prioriza el *recall* en riesgo alto (es peor no detectar una zona en riesgo que sobreestimarla).
- **Comparar siempre contra la línea base** (regresión lineal) para demostrar la ganancia del modelo principal.

---

## 6. Simulación de escenarios

El modelo entrenado se usa como **simulador**: se modifican las variables de entrada y se vuelve a predecir.

### Escenario A — Sin intervención
- Proyectar las variables sociodemográficas con su tendencia actual (o mantenerlas constantes).
- Predecir la participación esperada en la siguiente elección.
- Resultado: mapa de riesgo "inercial".

### Escenario B — Con intervención hipotética
Modificar únicamente variables **accionables** por la autoridad electoral, por ejemplo:

| Intervención | Variable modificada | Ejemplo de supuesto |
|---|---|---|
| Ampliar casillas en zonas rurales | Casillas por 1 000 electores | +1 casilla por cada 750 electores en secciones rurales |
| Campaña de información cívica a jóvenes | Indicador de exposición informativa | +5 puntos en secciones con >30 % de población 18–29 |
| Módulos itinerantes de credencialización | Cobertura de lista nominal | +3 % de lista nominal en secciones de alta marginación |
| Voto anticipado / casillas especiales | Accesibilidad | Reducción de distancia promedio a casilla |

### Escenario C (opcional) — Incertidumbre con Monte Carlo
- Perturbar las variables con ruido aleatorio en N iteraciones (ej. 1 000).
- Reportar intervalos (percentiles 5–95) en lugar de un solo número.
- Permite decir: "con 90 % de confianza, la participación en esta sección estará entre 42 % y 51 %".

**Resultado de la simulación:** para cada territorio, la diferencia de participación esperada entre el escenario A y el B = impacto estimado de la intervención.

---

## 7. Esquema de riesgo territorial

### 7.1 Clasificación
- **Semáforo de tres niveles** a partir del valor predicho:
  - 🔴 **Riesgo alto:** participación esperada por debajo del percentil 33 (o caída > 5 puntos vs. elección anterior).
  - 🟡 **Riesgo medio:** entre percentil 33 y 66.
  - 🟢 **Riesgo bajo:** por encima del percentil 66.
- Los umbrales pueden ser relativos (cuantiles) o fijos (definidos con el INE).

### 7.2 Perfiles de riesgo (clustering)
- Aplicar **K-Means** o **clustering jerárquico** sobre las variables sociodemográficas de las secciones en riesgo alto.
- Se obtienen perfiles tipo, por ejemplo:
  - *"Urbano joven con baja participación histórica"*
  - *"Rural con baja accesibilidad a casillas"*
  - *"Alta marginación y baja escolaridad"*
  - *"Alta movilidad / población migrante"*
- Cada perfil recibe un paquete de recomendaciones distinto.

### 7.3 Visualización
- Mapa coroplético por sección/municipio con el semáforo.
- Capa de comparación: escenario sin intervención vs. con intervención.
- Ficha por territorio con: participación histórica, predicción, nivel de riesgo, top 3 factores SHAP, perfil de clúster y recomendaciones.

---

## 8. Recomendaciones preventivas

Las recomendaciones se derivan de los factores SHAP y del perfil de clúster de cada territorio:

| Factor dominante | Recomendación preventiva |
|---|---|
| Baja accesibilidad (pocas casillas, distancia) | Instalación de casillas adicionales o extraordinarias; transporte comunitario el día de la jornada |
| Alta proporción de jóvenes con baja participación | Campañas digitales segmentadas; brigadas en universidades y preparatorias; credencialización en planteles |
| Baja escolaridad / alta marginación | Materiales informativos en lenguaje sencillo y lenguas indígenas; promotores comunitarios |
| Alta movilidad / migración | Difusión de voto desde el extranjero y casillas especiales; módulos de actualización de domicilio |
| Tendencia sostenida a la baja | Diagnóstico cualitativo focalizado (grupos de enfoque); alianzas con organizaciones locales |
| Alto porcentaje de votos nulos | Capacitación sobre cómo marcar la boleta; campañas de confianza en el proceso |

### Uso de LLM para redacción
- Se puede usar un modelo de lenguaje (API de OpenAI / Anthropic / Google, o Llama en local) para **redactar** las recomendaciones en lenguaje natural a partir del perfil SHAP y clúster de cada territorio.
- Debe quedar explícito en la presentación: **el LLM redacta, no predice.** La predicción proviene del modelo estadístico auditable.

---

## 9. Stack tecnológico propuesto

| Capa | Herramientas |
|---|---|
| Lenguaje | Python 3.11+ |
| Datos | `pandas`, `numpy`, `geopandas` |
| Modelado | `scikit-learn`, `lightgbm` (o `xgboost` / `catboost`) |
| Explicabilidad | `shap` |
| Visualización | `folium`, `plotly`, `matplotlib` |
| Dashboard / demo | `streamlit` (o integrar en Django con API REST) |
| Notebooks | Jupyter para exploración y prototipado |
| Control de versiones | Git |

---

## 10. Plan de trabajo sugerido (hackathon)

| Fase | Actividades | Entregable |
|---|---|---|
| 1. Datos | Descargar participación INE, Censo INEGI, marginación CONAPO, cartografía. Unir por clave de sección/municipio. | Dataset limpio |
| 2. Exploración | Estadísticas descriptivas, correlaciones, mapa de participación histórica. | Notebook EDA |
| 3. Modelo base | Regresión lineal con validación temporal. | Métricas base |
| 4. Modelo principal | LightGBM + ajuste ligero de hiperparámetros + SHAP. | Modelo entrenado y explicado |
| 5. Escenarios | Implementar escenario A, B y (opcional) Monte Carlo. | Tabla de impacto por territorio |
| 6. Esquema territorial | Semáforo, clustering de perfiles, mapa interactivo. | Mapa de riesgo |
| 7. Recomendaciones | Matriz factor → acción; redacción (opcionalmente con LLM). | Documento de recomendaciones |
| 8. Presentación | Dashboard en Streamlit + pitch. | Demo |

---

## 11. Argumento de valor para el jurado

- **Simple y explicable:** modelo de boosting con SHAP; cada predicción se puede justificar.
- **Accionable:** las variables simuladas son las que la autoridad electoral realmente puede modificar.
- **Territorial:** resultados a nivel sección con mapa y perfiles de riesgo.
- **Ético:** datos abiertos y agregados; sin información personal; sin sesgo partidista.
- **Escalable:** el mismo flujo sirve para elecciones federales, locales y para actualizarse con cada nuevo proceso.

---

## 12. Riesgos y consideraciones

| Riesgo | Mitigación |
|---|---|
| Pocas elecciones históricas por sección | Usar variables de tendencia agregadas; combinar niveles (sección + municipio) |
| Cambios en la cartografía electoral entre elecciones (reseccionamiento) | Usar tablas de equivalencia del INE o trabajar a nivel municipio donde no haya continuidad |
| Sobreajuste del boosting | Validación temporal, regularización, comparación con línea base |
| Interpretación indebida (estigmatizar territorios) | Presentar el riesgo como oportunidad de intervención, no como etiqueta; comunicar intervalos de incertidumbre |
| Supuestos de la intervención hipotética | Documentar explícitamente cada supuesto y permitir modificarlo en el dashboard |
