-- =====================================================================
-- estructura_inicial.sql  |  HRTech People Analytics (Guía 1)
-- Base de datos SQLite: datos/crudos/empresa_hr_analytics.db
-- Uso:  sqlite3 datos/crudos/empresa_hr_analytics.db < sql/estructura_inicial.sql
-- =====================================================================

CREATE TABLE IF NOT EXISTS capacitaciones (
    id_capacitacion INTEGER PRIMARY KEY,
    id_empleado     INTEGER NOT NULL,
    curso           TEXT    NOT NULL,
    horas           INTEGER NOT NULL,
    resultado       TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_capacitaciones_empleado
    ON capacitaciones (id_empleado);

INSERT OR REPLACE INTO capacitaciones
    (id_capacitacion, id_empleado, curso, horas, resultado)
VALUES
    (1,  1,  'Excel avanzado',          10, 'Aprobado'),
    (2,  2,  'Comunicación efectiva',    8, 'Aprobado'),
    (3,  3,  'Liderazgo',               12, 'Reprobado'),
    (4,  4,  'Trabajo en equipo',        6, 'Aprobado'),
    (5,  5,  'Power BI',                10, 'Aprobado'),
    (6,  6,  'Gestión del tiempo',       6, 'Aprobado'),
    (7,  7,  'Resolución de conflictos', 8, 'Reprobado'),
    (8,  8,  'Inteligencia emocional',   8, 'Aprobado'),
    (9,  9,  'Análisis de datos',       12, 'Aprobado'),
    (10, 10, 'Seguridad informática',   10, 'Aprobado');
