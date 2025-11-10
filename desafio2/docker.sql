CREATE TABLE IF NOT EXISTS registros (
    id SERIAL PRIMARY KEY,
    mensagem TEXT
);

INSERT INTO registros (mensagem) VALUES ('Primeiro registro persistido.');