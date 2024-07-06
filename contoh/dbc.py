import mysql.connector
from mysql.connector import Error

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kantor"
    )

def fetch_data(table="dosen"):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def save_data(table, data):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        if table == "pegawai":
            query = "INSERT INTO pegawai (nama, alamat, jabatan) VALUES (%s, %s, %s)"
        elif table == "dosen":
            query = "INSERT INTO dosen (nama, alamat, mata_kuliah, no_telpon, jabatan, foto) VALUES (%s, %s, %s, %s, %s, %s)"
        
        print("Query:", query)  # Debugging: Print query
        print("Data:", data)    # Debugging: Print data

        cursor.execute(query, data)
        conn.commit()  # Commit transaction

        print("Data berhasil disimpan!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

def update_data(table, data, id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        if table == "pegawai":
            query = "UPDATE pegawai SET nama=%s, alamat=%s, jabatan=%s WHERE id=%s"
        elif table == "dosen":
            query = "UPDATE dosen SET nama=%s, alamat=%s, mata_kuliah=%s, no_telpon=%s, jabatan=%s, foto=%s WHERE id=%s"
        
        print("Query:", query)       # Debugging: Print query
        print("Data:", data + (id,)) # Debugging: Print data

        cursor.execute(query, data + (id,))
        conn.commit()  # Commit transaction

        print("Data berhasil diperbarui!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

def delete_data(table, id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM {table} WHERE id=%s"
        cursor.execute(query, (id,))
        conn.commit()  # Commit transaction

        print(f"Data dengan ID {id} berhasil di update!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

