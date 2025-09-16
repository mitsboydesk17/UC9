# auth.py

import mysql.connector
from mysql.connector import Error, IntegrityError
from db import conectar  # Função de conexão com o banco (já existe)
import bcrypt

def hash_senha(senha):
    """Gera um hash seguro para a senha"""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha, senha_hash):
    """Verifica se a senha bate com o hash armazenado"""
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())

# ---------------------------
# Visitante - Cadastro
# ---------------------------

def cadastrar_visitante(nome, cpf, data_nasc, telefone, email, senha):
    senha_hash = hash_senha(senha)
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = '''
        INSERT INTO Visitante (nome, cpf, data_nascimento, telefone, email, senha_hash)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        valores = (nome, cpf, data_nasc, telefone, email, senha_hash)
        cursor.execute(sql, valores)

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Cadastro de visitante realizado com sucesso!"

    except IntegrityError:
        return False, "Email ou CPF já cadastrado."
    except Error as err:
        return False, f"Erro no cadastro: {err}"

# ---------------------------
# Funcionário - Cadastro
# ---------------------------

def cadastrar_funcionario(nome, cargo, email, senha, salario):
    try:
        conn = conectar()
        cursor = conn.cursor()

        senha_hash = hash_senha(senha)
        sql = '''
        INSERT INTO Funcionario (nome, cargo, email, senha_hash, salario, data_contratacao, ativo)
        VALUES (%s, %s, %s, %s, %s, CURDATE(), TRUE)
        '''
        valores = (nome, cargo, email, senha_hash, float(salario))
        cursor.execute(sql, valores)

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Funcionário cadastrado com sucesso!"
    except IntegrityError:
        return False, "Email já cadastrado."
    except Error as err:
        return False, f"Erro no cadastro: {err}"

# ---------------------------
# Login Unificado (Visitante + Funcionario)
# ---------------------------

def verificar_login(email, senha):
    """Verifica login tanto de visitante quanto de funcionário"""
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Tentar Visitante
        sql_visitante = '''
        SELECT id, nome, senha_hash FROM Visitante WHERE email = %s
        '''
        cursor.execute(sql_visitante, (email,))
        visitante = cursor.fetchone()

        if visitante:
            id, nome, senha_hash = visitante
            if verificar_senha(senha, senha_hash):
                cursor.close()
                conn.close()
                return True, ('visitante', id, nome)

        # Tentar Funcionário
        sql_funcionario = '''
        SELECT id, nome, cargo, senha_hash FROM Funcionario WHERE email = %s AND ativo = TRUE
        '''
        cursor.execute(sql_funcionario, (email,))
        funcionario = cursor.fetchone()

        cursor.close()
        conn.close()

        if funcionario:
            id, nome, cargo, senha_hash = funcionario
            if verificar_senha(senha, senha_hash):
                return True, ('funcionario', id, nome, cargo)

        # Se não encontrou ou senha errada
        return False, "Email ou senha incorretos."

    except Error as err:
        return False, f"Erro no login: {err}"

# ---------------------------
# Cadastro de Atração
# ---------------------------

def cadastrar_atracao(nome, descricao, capacidade, restricao_altura, horario_func):
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = '''
        INSERT INTO Atracao (nome, descricao, capacidade, restricao_altura, horario_funcionamento)
        VALUES (%s, %s, %s, %s, %s)
        '''
        valores = (nome, descricao, int(capacidade), float(restricao_altura), horario_func)
        cursor.execute(sql, valores)

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Atração cadastrada com sucesso!"
    except Error as err:
        return False, f"Erro ao cadastrar atração: {err}"

# ---------------------------
# Listagem de Visitantes
# ---------------------------

def listar_visitantes():
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = 'SELECT id, nome, cpf, data_nascimento, telefone, email FROM Visitante'
        cursor.execute(sql)
        resultado = cursor.fetchall()

        cursor.close()
        conn.close()
        return resultado
    except Error:
        return []
