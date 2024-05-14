import pymysql.cursors
import json

# from utils import logging
import logging
import local_secrets as secrets

DB_SECRETS = secrets.DB_SECRETS

logger = logging.getLogger()


##### CONNECTIONS #####


def get_connection():
    conn = pymysql.connect(
        user=DB_SECRETS["DB_USER"],
        password=DB_SECRETS["DB_PASSWORD"],
        host=DB_SECRETS["DB_HOST"],
        database=DB_SECRETS["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


def close_connection(conn):
    conn.close()


def l_to_d(keys, values):
    return dict(zip(keys, values))


##### USER #####


def insert_user(
    user_email,
    user_id_google,
    user_first_name,
    user_last_name,
    access_token,
    refresh_token,
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            res = cursor.execute(
                """
                    INSERT INTO user (user_email, user_id_google, user_first_name, user_last_name, access_token, refresh_token) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_email,
                    user_id_google,
                    user_first_name,
                    user_last_name,
                    access_token,
                    refresh_token,
                ),
            )
            conn.commit()
            user_id = cursor.lastrowid
    except Exception as e:
        print("***************************")
        print(user_email)
        print("DB error in insert_user:\n", str(e))
        raise
    return user_id


def get_user_by_google_user_id(user_id_google):
    query_string = """
                    SELECT *
                    FROM user
                    WHERE user_id_google = %s
                """
    try:
        print("getting connection")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query_string, (user_id_google,))
        rows = cur.fetchall()
    except Exception as e:
        print("db.get_user ERROR:", e)
        return {"result": "DB_CONNECTION_ERROR"}
    close_connection(conn)
    if len(rows) == 0:
        return {"result": "USER_NOT_FOUND"}
    if len(rows) == 2:
        return {"result": "TOO_MANY_ROWS"}
    rows[0]["result"] = "SUCCESS"
    return rows[0]


def validate_user(user_name, password):
    query_string = """
                    SELECT user_id, user_name, password,
                        user_description, domain_id
                    FROM user
                    WHERE user_name = %s
                """
    try:
        print("getting connection")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query_string, (user_name,))
        rows = cur.fetchall()
    except Exception as e:
        return {"error": "DB_CONNECTION_ERROR"}
    close_connection(conn)

    if len(rows) == 0:
        return {"error": "USER_NOT_FOUND"}
    elif len(rows) > 1:
        return {"error": "DB_ERROR"}
    elif rows[0]["password"] != password:
        return {"error": "INVALID_PASSWORD"}
    user = rows[0]
    del user["password"]
    return user


##### DOCUMENT PIPELINE #####


def delete_document(doc_id):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = f"DELETE FROM document_chunk WHERE doc_id = %s"
            res = cursor.execute(sql, (doc_id,))
            sql = f"DELETE FROM document WHERE doc_id = %s"
            res = cursor.execute(sql, (doc_id,))
            conn.commit()
    except pymysql.Error as e:
        print(f"Error deleting row: {e}")
        raise
    return res


def get_all_docs_from_domain(conn, domain_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT doc_id, domain_id, doc_uri, doc_title, doc_text FROM document WHERE domain_id = %s",
        (domain_id,),
    )
    rows = cur.fetchall()
    res = [
        (
            row["doc_id"],
            row["domain_id"],
            row["doc_uri"],
            row["doc_title"],
            row["doc_text"],
        )
        for row in rows
    ]
    return res


def insert_document_chunk(doc_id, chunk_text, chunk_embedding):
    json_data = json.dumps(chunk_embedding)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO document_chunk (doc_id, chunk_text, chunk_embedding) VALUES (%s, %s, %s)",
        (doc_id, chunk_text, json_data),
    )
    conn.commit()
    return cur.lastrowid


def update_document_chunk_embedding(conn, doc_chunk_id, embedding):
    json_data = json.dumps(embedding)
    cur = conn.cursor()
    cur.execute(
        "UPDATE document_chunk SET chunk_embedding = %s WHERE doc_chunk_id = %s",
        (
            json_data,
            doc_chunk_id,
        ),
    )
    conn.commit()
