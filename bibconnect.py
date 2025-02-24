
def conectar():
    import pyodbc
    condutor="odbc driver 17 for sql server"
    servidor=r"Hummer\SQLEXPRESS"
    db="turma94"
    user="py2sql"
    senha="12345"

    try:
        con = pyodbc.connect(f"DRIVER={condutor};SERVER={servidor};DATABASE={db};UID={user};PWD={senha};Encrypt=no;",autocommit=True)
        return con
    except:
        return False