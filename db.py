import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kantor"
    )

def fetch_data(table):
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
    if table == "pegawai":
        query = "INSERT INTO pegawai (nama, alamat, jabatan) VALUES (%s, %s, %s)"
    elif table == "dosen":
        query = "INSERT INTO dosen (nama, alamat, mata_kuliah, no_telpon) VALUES (%s, %s,%s, %s)"
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

def update_data(table, data, id):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            if table == "pegawai":
                query = "UPDATE pegawai SET nama=%s, alamat=%s, jabatan=%s WHERE id=%s"
            elif table == "dosen":
                query = "UPDATE dosen SET nama=%s, alamat=%s, mata_kuliah=%s, no_telpon=%s WHERE id=%s"
            cursor.execute(query, data + (id,))  # Ensure the order of data matches the query
            conn.commit()
        else:
            print("Connection to database failed.")
    except mysql.connector.Error as err:
        print(f"Error updating data in {table}: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()


def delete_data(table, id):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"DELETE FROM {table} WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
