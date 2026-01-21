CREATE DATABASE IF NOT EXISTS prueba_tecnica;
USE prueba_tecnica;

CREATE TABLE historia (
  identificacion VARCHAR(20),
  corte_mes DATE,
  saldo DECIMAL(15,2)
);

CREATE TABLE retiros (
  identificacion VARCHAR(20),
  fecha_retiro DATE
);

SELECT * FROM historia LIMIT 10;
SELECT * FROM retiros LIMIT 10;

WITH RECURSIVE

-- se normaliza la columna corte_mes para que no de problemas al compararla con otras fechas
historia_mes AS (
  SELECT
    identificacion,
    DATE_FORMAT(corte_mes, '%Y-%m-01') AS corte_mes,
    saldo
  FROM historia
),

-- Se calcula la fecha de primera aparición del cliente
primera_aparicion AS (
  SELECT
    identificacion,
    MIN(corte_mes) AS fecha_inicio
  FROM historia_mes
  GROUP BY identificacion
),

--  Calendario general
calendario AS (
  SELECT (SELECT MIN(fecha_inicio) FROM primera_aparicion) AS corte_mes
  UNION ALL
  SELECT DATE_ADD(corte_mes, INTERVAL 1 MONTH)
  FROM calendario
  WHERE corte_mes < '2024-12-31'
),

-- Calendario por cliente desde su primera aparición
calendario_cliente AS (
  SELECT
    p.identificacion,
    c.corte_mes
  FROM primera_aparicion p
  JOIN calendario c
    ON c.corte_mes >= p.fecha_inicio
),

-- Filtrado por retiro, excluye los campos que tienen fecha de retiro y la fecha de corte es mayor a la fecha de retiro
calendario_filtrado AS (
  SELECT
    cc.identificacion,
    cc.corte_mes
  FROM calendario_cliente cc
  LEFT JOIN retiros r
    ON cc.identificacion = r.identificacion
  WHERE r.fecha_retiro IS NULL
     OR cc.corte_mes <= DATE_FORMAT(r.fecha_retiro, '%Y-%m-01')
),

-- En los meses que el saldo del cliente es nulo, se asigna cero
dataset_completo AS (
  SELECT
    cf.identificacion,
    cf.corte_mes,
    COALESCE(h.saldo, 0) AS saldo
  FROM calendario_filtrado cf
  LEFT JOIN historia_mes h
    ON cf.identificacion = h.identificacion
   AND cf.corte_mes = h.corte_mes
),

-- Clasificación FINAL por nivel 
dataset_final AS (
  SELECT
    identificacion,
    corte_mes,
    saldo,
    CASE
      WHEN saldo >= 0 AND saldo < 300000 THEN 'N0'
      WHEN saldo >= 300000 AND saldo < 1000000 THEN 'N1'
      WHEN saldo >= 1000000 AND saldo < 3000000 THEN 'N2'
      WHEN saldo >= 3000000 AND saldo < 5000000 THEN 'N3'
      WHEN saldo >= 5000000 THEN 'N4'
    END AS nivel
  FROM dataset_completo
),

-- Se crea una columna llamada grp, cada que el valor de grp cambia, significa que empieza una nueva racha
racha_base AS (
  SELECT
    identificacion,
    corte_mes,
    nivel,
    ROW_NUMBER() OVER (PARTITION BY identificacion ORDER BY corte_mes) -
    ROW_NUMBER() OVER (PARTITION BY identificacion, nivel ORDER BY corte_mes) AS grp
  FROM dataset_final
),

-- Usando la columna grp que se calculo anteriormente, se cuenta la cantidad de rachas que se dan, su fecha de inicio y fin
rachas AS (
  SELECT
    identificacion,
    nivel,
    MIN(corte_mes) AS fecha_inicio,
    MAX(corte_mes) AS fecha_fin,
    COUNT(*) AS racha
  FROM racha_base
  GROUP BY identificacion, nivel, grp
),

-- Se filtra por las rachas que son mayores o iguales a 3
rachas_validas AS (
  SELECT *
  FROM rachas
  WHERE racha >= 3   -- n
),

-- Lo que hace es que para un mismo cliente ordena las rachas mayores que ha tenido, dandole el primer puesto a la racha más larga
-- En caso de que el cliente tenga dos rachas iguales, pone primero a la racha más reciente
racha_final AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY identificacion
      ORDER BY racha DESC, fecha_fin DESC
    ) AS rn
  FROM rachas_validas
)

-- Consulta final
SELECT
  identificacion,
  racha,
  fecha_fin,
  nivel
FROM racha_final
WHERE rn = 1
ORDER BY racha DESC, fecha_fin DESC;







