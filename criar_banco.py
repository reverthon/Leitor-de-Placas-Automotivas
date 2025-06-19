import sqlite3

# Cria o banco e conecta
conn = sqlite3.connect('veiculos.db')
cursor = conn.cursor()

# Cria a tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS veiculos (
    placa TEXT PRIMARY KEY,
    dono TEXT,
    situacao TEXT
)
''')

# Dados de exemplo
veiculos_exemplo = [
    ('BRA2E19', 'João da Silva', 'Regular'),
    ('XYZ5678', 'Maria Oliveira', 'Multa Pendente'),
    ('DEF4321', 'Carlos Souza', 'Roubo/Furto')
]

# Inserir dados
for v in veiculos_exemplo:
    cursor.execute('INSERT OR IGNORE INTO veiculos VALUES (?, ?, ?)', v)

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
