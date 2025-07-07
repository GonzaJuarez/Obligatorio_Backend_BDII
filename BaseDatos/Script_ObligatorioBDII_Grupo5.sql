CREATE DATABASE IF NOT EXISTS XR_Grupo5;

USE XR_Grupo5;

CREATE TABLE IF NOT EXISTS Votante (
    CC VARCHAR(7) PRIMARY KEY,
    CI VARCHAR(20) NOT NULL ,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    fechaNacimiento DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Establecimiento (
    ID INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS circuito (
    ID INT PRIMARY KEY,
    departamento VARCHAR(100) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    accesible BOOLEAN NOT NULL,
    IDEstablecimiento INT NOT NULL,
    FOREIGN KEY (IDEstablecimiento) REFERENCES Establecimiento(ID)
);

CREATE TABLE IF NOT EXISTS miembroMesa (
    CC VARCHAR(7) PRIMARY KEY,
    organismoEstado VARCHAR(100) NOT NULL,
    IDCircuito INT NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol ENUM('OPERADOR', 'ADMIN') NOT NULL,
    FOREIGN KEY (CC) REFERENCES Votante(CC),
    FOREIGN KEY (IDCircuito) REFERENCES circuito(ID)
);

CREATE TABLE IF NOT EXISTS agentePolicia (
    CC VARCHAR(7) PRIMARY KEY,
    IDEstablecimiento INT NOT NULL,
    Comisaria VARCHAR(100) NOT NULL,
    FOREIGN KEY (CC) REFERENCES Votante(CC),
    FOREIGN KEY (IDEstablecimiento) REFERENCES Establecimiento(ID)
);

CREATE TABLE IF NOT EXISTS integranteLista (
    CC VARCHAR(7) PRIMARY KEY,
    FOREIGN KEY (CC) REFERENCES Votante(CC)
);

CREATE TABLE IF NOT EXISTS partidoPolitico (
    ID INT PRIMARY KEY,
    direccionSede VARCHAR(255) NOT NULL,
    autoridades TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidato (
    CC VARCHAR(7) PRIMARY KEY,
    IDPartidoPolitico INT NOT NULL,
    FOREIGN KEY (CC) REFERENCES Votante(CC),
    FOREIGN KEY (IDPartidoPolitico) REFERENCES partidoPolitico(ID)
);

CREATE TABLE IF NOT EXISTS eleccion (
    ID INT PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS lista (
    numero INT,
    IDEleccion INT,
    departamento VARCHAR(100) NOT NULL,
    IDPartidoPolitico INT NOT NULL,
    CCCandidato VARCHAR(20) NOT NULL,
    PRIMARY KEY (numero, IDEleccion),
    FOREIGN KEY (IDPartidoPolitico) REFERENCES partidoPolitico(ID),
    FOREIGN KEY (IDEleccion) REFERENCES eleccion(ID),
    FOREIGN KEY (CCCandidato) REFERENCES candidato(CC)
);

CREATE TABLE IF NOT EXISTS integra (
    CC VARCHAR(7),
    numeroLista INT,
    ordenIntegrantes INT NOT NULL,
    organo VARCHAR(100) NOT NULL,
    PRIMARY KEY (CC, numeroLista),
    FOREIGN KEY (CC) REFERENCES integranteLista(CC),
    FOREIGN KEY (numeroLista) REFERENCES lista(numero)
);

CREATE TABLE IF NOT EXISTS voto (
    ID INT PRIMARY KEY,
    fechaHora TIMESTAMP NOT NULL,
    IDCircuito INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    observado TEXT NOT NULL,
    FOREIGN KEY (IDCircuito) REFERENCES circuito(ID)
);

CREATE TABLE IF NOT EXISTS incluye (
    IDVoto INT,
    numeroLista INT,
    PRIMARY KEY (IDVoto, numeroLista),
    FOREIGN KEY (IDVoto) REFERENCES voto(ID),
    FOREIGN KEY (numeroLista) REFERENCES lista(numero)
);

CREATE TABLE IF NOT EXISTS listaCredenciales (
    CC VARCHAR(7),
    IDCircuito INT,
    PRIMARY KEY (CC, IDCircuito),
    FOREIGN KEY (CC) REFERENCES Votante(CC),
    FOREIGN KEY (IDCircuito) REFERENCES circuito(ID)
);

CREATE TABLE IF NOT EXISTS registroDeEmision (
    CC VARCHAR(7),
    IDEleccion INT,
    fechaHora TIMESTAMP NOT NULL,
    IDCircuito INT NOT NULL,
    PRIMARY KEY (CC, IDEleccion),
    FOREIGN KEY (CC) REFERENCES Votante(CC),
    FOREIGN KEY (IDEleccion) REFERENCES eleccion(ID),
    FOREIGN KEY (IDCircuito) REFERENCES circuito(ID)
);
