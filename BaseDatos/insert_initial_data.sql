USE XR_Grupo5;

-- Insertar votantes (necesarios para operadores y agentes)
INSERT INTO Votante (CC, CI, nombre, direccion, fechaNacimiento) VALUES
('ABC1111', '12345678', 'Admin', 'Sistema', '1990-01-01'),
('ABC1112', '23456789', 'Juan', 'Pérez', '1985-05-15'),
('ABC1113', '34567890', 'María', 'González', '1988-08-22'),
('ABC1114', '45678901', 'Carlos', 'López', '1992-03-10'),
('ABC1115', '56789012', 'Ana', 'Martínez', '1987-12-05'),
('ABC1116', '67890123', 'Roberto', 'Rodríguez', '1995-07-18'),
('ABC1117', '78901234', 'Laura', 'Fernández', '1983-11-30'),
('ABC1118', '89012345', 'Miguel', 'García', '1991-04-25'),
('ABC1119', '90123456', 'Patricia', 'Hernández', '1986-09-12'),
('ABC1120', '01234567', 'Alejandro', 'Silva', '1993-06-08'),
('ABC1121', '11111111', 'Carmen', 'Vargas', '1989-02-14'),
('ABC1122', '22222222', 'Diego', 'Morales', '1994-10-20'),
('ABC1123', '33333333', 'Elena', 'Castro', '1984-07-03'),
('ABC1124', '44444444', 'Francisco', 'Reyes', '1996-12-25'),
('ABC1125', '55555555', 'Gabriela', 'Torres', '1982-04-18'),
('ABC1126', '66666666', 'Marcelo', 'Garcia', '1982-04-18'),
('ABC1127', '77777777', 'Pedro', 'Gonzalez', '1982-04-18'),
('ABC1128', '88888888', 'Gonzalo', 'Juarez', '1982-04-18'),
('ABC1129', '99999999', 'Florencia', 'Correa', '1982-04-18'),
('ABC1130', '00000000', 'Jaun Pablo', 'Cerizola', '1982-04-18'),
('ABC1131', '11111111', 'Leon', 'Salvo', '1982-04-18');

-- Insertar establecimientos
INSERT INTO Establecimiento (ID, nombre) VALUES
(1, 'Escuela Primaria N°1'),
(2, 'Colegio Secundario N°2'),
(3, 'Universidad Nacional'),
(4, 'Centro Comunitario Norte'),
(5, 'Instituto Técnico Sur'),
(6, 'Escuela Rural Este'),
(7, 'Centro Cultural Oeste');

-- Insertar circuitos electorales
INSERT INTO circuito (ID, departamento, localidad, direccion, barrio, accesible, IDEstablecimiento) VALUES
(1, 'Capital', 'Centro', 'Av. Principal 123', 'Centro', TRUE, 1),
(2, 'Capital', 'Norte', 'Calle Secundaria 456', 'Norte', TRUE, 2),
(3, 'Interior', 'Ciudad Norte', 'Campus Universitario 789', 'Universitario', TRUE, 3),
(4, 'Interior', 'Pueblo Norte', 'Plaza Norte 321', 'Plaza', FALSE, 4),
(5, 'Interior', 'Villa Sur', 'Ruta Sur 654', 'Villa', TRUE, 5),
(6, 'Interior', 'Campo Este', 'Camino Rural 987', 'Rural', FALSE, 6),
(7, 'Interior', 'Pueblo Oeste', 'Boulevard Oeste 147', 'Boulevard', TRUE, 7);

-- Insertar operadores (miembros de mesa)
-- Password hash para 'admin123' usando bcrypt
INSERT INTO miembroMesa (CC, organismoEstado, IDCircuito, password, rol) VALUES
('ABC1111', 'Corte Electoral Nacional', 1, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', 'ADMIN'),
('ABC1112', 'Corte Electoral Departamental', 2, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', 'OPERADOR'),
('ABC1113', 'Corte Electoral Departamental', 3, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', 'OPERADOR'),
('ABC1114', 'Corte Electoral Departamental', 4, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2O', 'OPERADOR');

-- Insertar agentes de policía
INSERT INTO agentePolicia (CC, IDEstablecimiento, Comisaria) VALUES
('ABC1115', 1, 'Comisaría Central'),
('ABC1116', 1, 'Comisaría Central'),
('ABC1117', 2, 'Comisaría Norte'),
('ABC1118', 3, 'Comisaría Universitaria'),
('ABC1119', 4, 'Comisaría Rural Norte'),
('ABC1120', 5, 'Comisaría Sur'),
('ABC1121', 6, 'Comisaría Rural Este'),
('ABC1122', 7, 'Comisaría Oeste');

-- Insertar partidos políticos
INSERT INTO partidoPolitico (ID, direccionSede, autoridades) VALUES
(1, 'Av. Libertad 123, Capital', 'Presidente: Dr. Gonzalo Juarez\nVicepresidente: Lic. Florencia Correa'),
(2, 'Calle República 456, Capital', 'Presidente: Ing. Juan Pablo Cerizola\nVicepresidente: Dr. Leon Salvo');

-- Insertar candidatos
INSERT INTO candidato (CC, IDPartidoPolitico) VALUES
('ABC1128', 1),
('ABC1129', 1),
('ABC1130', 2),
('ABC1131', 2);

-- Insertar integrantes de listas
INSERT INTO integranteLista (CC) VALUES
('ABC1112'),
('ABC1113'),
('ABC1114'),
('ABC1115'),
('ABC1116'),
('ABC1117'),
('ABC1118'),
('ABC1119'),
('ABC1120'),
('ABC1121'),
('ABC1122'),
('ABC1123'),
('ABC1124'),
('ABC1125'),
('ABC1126'),
('ABC1127');

-- Insertar elecciones
INSERT INTO eleccion (ID, fecha, tipo) VALUES
(1, '2024-11-10', 'Elecciones Precidenciales');

-- Insertar listas electorales
INSERT INTO lista (numero, IDEleccion, departamento, IDPartidoPolitico, CCCandidato) VALUES
(101, 1, 'Durazno', 1, 'ABC1128'),
(102, 1, 'Maldonado', 1, 'ABC1128'),
(103, 1, 'Montevideo', 1, 'ABC1128'),
(104, 1, 'Canelones', 1, 'ABC1128'),
(201, 1, 'Durazno', 2, 'ABC1130'),
(202, 1, 'Maldonado', 2, 'ABC1130'),
(203, 1, 'Montevideo', 2, 'ABC1130'),
(204, 1, 'Canelones', 2, 'ABC1130');

-- Insertar relaciones integra (integrantes en listas)
INSERT INTO integra (CC, numeroLista, ordenIntegrantes, organo) VALUES
('ABC1112', 101, 1, 'Presidencia'),
('ABC1113', 101, 2, 'Vicepresidencia'),
('ABC1114', 102, 1, 'Presidencia'),
('ABC1115', 102, 2, 'Vicepresidencia'),
('ABC1116', 103, 1, 'Presidencia'),
('ABC1117', 103, 2, 'Vicepresidencia'),
('ABC1118', 104, 1, 'Presidencia'),
('ABC1119', 104, 2, 'Vicepresidencia'),
('ABC1120', 201, 1, 'Presidencia'),
('ABC1121', 201, 2, 'Vicepresidencia'),
('ABC1122', 202, 1, 'Presidencia'),
('ABC1123', 202, 2, 'Vicepresidencia'),
('ABC1124', 203, 1, 'Presidencia'),
('ABC1125', 203, 2, 'Vicepresidencia'),
('ABC1126', 204, 1, 'Presidencia'),
('ABC1127', 204, 2, 'Vicepresidencia');

-- Insertar votos (ejemplo de votos emitidos)
INSERT INTO voto (ID, fechaHora, IDCircuito, estado, observado) VALUES
(1, '2024-09-15 09:30:00', 1, 'VALIDO', FALSE),
(2, '2024-09-15 10:15:00', 1, 'VALIDO', FALSE),
(3, '2024-09-15 11:45:00', 2, 'VALIDO', FALSE),
(4, '2024-09-15 12:20:00', 3, 'VALIDO', FALSE),
(5, '2024-09-15 13:10:00', 4, 'VALIDO', FALSE),
(6, '2024-09-15 14:05:00', 5, 'VALIDO', FALSE),
(7, '2024-09-15 15:30:00', 6, 'VALIDO', FALSE),
(8, '2024-09-15 16:45:00', 7, 'VALIDO', FALSE);

-- Insertar relaciones incluye (votos por lista)
INSERT INTO incluye (IDVoto, numeroLista) VALUES
(1, 101),
(2, 203),
(3, 203),
(4, 201),
(5, 101),
(6, 204),
(7, 102),
(8, 103);

-- Insertar lista de credenciales (votantes habilitados por circuito)
INSERT INTO listaCredenciales (CC, IDCircuito) VALUES
('ABC1112', 1),
('ABC1113', 1),
('ABC1114', 2),
('ABC1115', 2),
('ABC1116', 3),
('ABC1117', 3),
('ABC1118', 4),
('ABC1129', 4),
('ABC1120', 5),
('ABC1121', 5),
('ABC1122', 6),
('ABC1123', 6),
('ABC1124', 7),
('ABC1125', 7),
('ABC1126', 1);

-- Insertar registros de emisión (votos ya emitidos)
INSERT INTO registroDeEmision (CC, IDEleccion, fechaHora, IDCircuito) VALUES
('ABC1112', 1, '2024-09-15 09:30:00', 1),
('ABC1113', 1, '2024-09-15 10:15:00', 1),
('ABC1114', 1, '2024-09-15 11:45:00', 2),
('ABC1115', 1, '2024-09-15 12:20:00', 2),
('ABC1116', 1, '2024-09-15 13:10:00', 3),
('ABC1117', 1, '2024-09-15 14:05:00', 3),
('ABC1118', 1, '2024-09-15 15:30:00', 4),
('ABC1119', 1, '2024-09-15 16:45:00', 4);

-- Usuario administrador:
-- CC: 1234567
-- Password: admin123 (hash incluido)
-- Rol: ADMIN