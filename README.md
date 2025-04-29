# Documentacion de Nuestro Proyecto de regresión

<center>
<img src="https://github.com/user-attachments/assets/fc7e8638-a11c-493d-b3cf-a9845c3d02c6" width="300">
</center>
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/mikewig">
        <img src="https://avatars.githubusercontent.com/u/198570893?v=4" width="100px;" alt="Maikel López"/>
        <br />
        <sub><b>Michael Lópe</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/andalons">
        <img src="https://avatars.githubusercontent.com/u/81816962?v=4" width="100px;" alt="Andrea Alonso"/>
        <br />
        <sub><b>Andrea Alonso</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/stephyangeles">
        <img src="https://avatars.githubusercontent.com/u/150821141?v=4" width="100px;" alt="Stephany Angeles"/>
        <br />
        <sub><b>Stephany Angeles</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/fintihlupik">
        <img src="https://avatars.githubusercontent.com/u/53350261?v=4" width="100px;" alt="Polina"/>
        <br />
        <sub><b>Polina</b></sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/juancmacias">
        <img src="https://avatars.githubusercontent.com/u/53483587?v=4" width="100px;" alt="Juan Carlos"/>
        <br />
        <sub><b>Juan Carlos Macías</b></sub>
      </a>
    </td>
  </tr>
</table>

Collab:
https://colab.research.google.com/drive/1qSKzDkcqzxyWBpg038GeAQpOfKLDT0Rt?usp=sharing

Despliegue:
https://p5-regresion-g4.onrender.com

## Crear y activar EV 
### Windows
```
python -m venv .venv

.venv/Scripts/activate
```


### Mac
```
python(3) -m venv .venv
source .venv/bin/activate
```

##Instalar dependencias txt

```
pip install requirements.txt
```


## Iniciar Docker desktop, instalar extension en vsc e iniciar
```
docker compose up --build
```


🛠️ Tecnologías a usar

Jupyter Notebook, Kaggle Notebooks
Numpy, Pandas, sklearn, Optuna
Matplotlib, Pyplot, Seaborn

🏆 Niveles de Entrega

🟢 Nivel Esencial:

  - ✅ Un modelo de ML funcional que prediga una variable numérica (ej: precio de una casa, ventas, tiempo de entrega, etc.).
  
  - ✅ Análisis exploratorio de los datos (EDA) con visualizaciones relevantes para regresión (scatter plots, distribución de la variable objetivo, correlaciones, etc.).
  
  - ✅ Overfitting inferior al 5% (diferencia aceptable entre métricas de entrenamiento y validación).
  
  - ✅ Una solución que productivice el modelo (Streamlit, Gradio, API, Dash, etc.).
  
  - ✅ Informe del rendimiento del modelo con métricas de regresión (RMSE, MAE, R², etc.) y explicación de su performance (feature importance, residuos, gráficos de predicción vs real).


🟡 Nivel Medio:

- ✅ Modelo de ML con técnicas de ensemble (Random Forest, Gradient Boosting, XGBoost, etc.).

- ✅ Uso de técnicas de Validación Cruzada (K-Fold, Leave-One-Out).

- ✅ Optimización del modelo con ajuste de hiperparámetros (GridSearch, RandomSearch, Bayesian Optimization).

- ✅❌ Sistema de recogida de feedback para monitorizar la performance del modelo en producción (métricas en tiempo real).

- ✅❌ Sistema de recogida de datos nuevos para futuros reentrenamientos (pipeline de ingestión de datos).


🟠 Nivel Avanzado:

- ✅ Versión dockerizada del programa.

- ✅🔸 (Guardado en log.txt, seguimiento de usuario) Guardado en bases de datos de los datos recogidos por la aplicación (SQL, MongoDB, etc.).

- ✅ Despliegue (AWS, GCP, Azure, render, vercel, etc.).

- ✅ Inclusión de test unitarios (validación de preprocesamiento, métricas mínimas aceptables, etc.).


🔴 Nivel Experto:

- ❌ Sistemas de entrenamiento y despliegue automático (MLOps) con:

- 🔹 A/B Testing para comparar modelos.

- 🔹 Monitoreo de Data Drift para detectar cambios en la distribución de los datos.

- 🔹 Auto-reemplazo de modelos solo si la nueva versión supera métricas predefinidas.




