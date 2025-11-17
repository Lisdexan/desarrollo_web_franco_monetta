-- Archivo: import.sql (FINAL)

-- 1. Insertar Avisos de Adopción (Se mantiene, ya que pasó la revisión de sintaxis)
INSERT INTO aviso_adopcion (id, fecha_publicacion, sector, cantidad, tipo, edad, comuna) VALUES (1, '2025-06-02', 'Beauchef 859, terraza', 1, 'Gato', '2 meses', 'Santiago');
INSERT INTO aviso_adopcion (id, fecha_publicacion, sector, cantidad, tipo, edad, comuna) VALUES (2, '2025-05-28', 'Plaza Maipu', 3, 'Perro', '2 meses', 'Maipu');

-- 2. Insertar Notas 
-- Corregimos el nombre de la columna de la nota a VALOR (o el nombre real de tu campo JPA)
-- Usamos mayúsculas para las columnas de la tabla 'nota' para evitar conflictos de caso en H2.
INSERT INTO nota (AVISO_ADOPCION_ID, VALOR) VALUES (1, 6);