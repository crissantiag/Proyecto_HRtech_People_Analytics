
# Politica de Gobernanza de Datos - HRTech People Analytics

## 1. Proposito
Definir como se usan, protegen, comparten y eliminan los datos de empleados
del proyecto HRTech People Analytics, minimizando el riesgo de exposicion
indebida de informacion personal, de desempeno y de compensacion.

## 2. Clasificacion de los datos
- **Publico**: agregados generales sin posibilidad de reidentificacion
  (ej. numero total de empleados por departamento).
- **Interno**: uso dentro del equipo de People Analytics
  (departamento, antiguedad, horas de capacitacion, horas extra).
- **Confidencial**: requiere proteccion y justificacion de uso
  (id_empleado, edad, estado_empleado, resultado de evaluaciones, satisfaccion).
- **Restringido**: acceso limitado a roles autorizados unicamente
  (nombre, salario, salario_anual, salario_por_hora, desempeño).

## 3. Acceso por rol
- **Administrador de RRHH**: acceso total al dataset crudo (identificado),
  bajo justificacion de negocio y registro de auditoria.
- **Analista de People Analytics**: acceso unicamente a la **vista
  analitica protegida** (`dataset_publicable_HRTech_People_Analytics.csv`),
  sin identificadores directos ni valores exactos de salario/edad/desempeño.
- **Auditor / Comite de etica**: acceso de solo lectura a la evidencia de
  gobernanza (clasificacion, matriz de riesgos, bitacoras), no a los datos
  crudos.
- **Empleado (titular del dato)**: derecho a solicitar que informacion
  personal propia le sea mostrada o corregida, conforme a los principios de
  transparencia.

## 4. Minimizacion
Solo se incluyen en la vista analitica los campos estrictamente necesarios
para los analisis de RRHH (rotacion, desempeño agregado, clima laboral,
capacitacion). Los identificadores directos y los valores exactos de
variables Restringidas se sustituyen por tokens, mascaras o rangos antes de
compartir cualquier dataset fuera del equipo de Administracion.

## 5. Retencion
- Datos de empleados **activos**: se conservan mientras dure la relacion
  laboral, mas el periodo minimo exigido por la normativa laboral/fiscal
  aplicable.
- Datos de empleados **inactivos**: se conservan un maximo definido por
  politica interna (ej. 2 anios) y luego se anonimizan o eliminan,
  salvo obligacion legal de conservarlos.
- Vistas analiticas protegidas: se regeneran a partir del dataset crudo
  cuando se requieran; no se mantienen copias antiguas sin control de
  version.

## 6. Etica
- No se toman decisiones automatizadas de contratacion, despido o ascenso
  basadas unicamente en los datos de este proyecto sin revision humana.
- No se usan variables sensibles (edad, salario, desempeño) para generar
  perfiles individuales fuera del proposito declarado de People Analytics.
- Las conclusiones se presentan siempre de forma agregada (por
  departamento, rango, categoria) y nunca senalando a un empleado en
  particular en reportes de uso general.
- Se revisa periodicamente que los criterios de evaluacion de desempeño no
  generen sesgos hacia algun departamento, rango de edad o antiguedad.
