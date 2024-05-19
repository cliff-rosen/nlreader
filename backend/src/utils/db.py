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
        print("get_user_by_google_user_id")
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


def update_user_authorization(user_id, credentials):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE  user
            SET     credentials = %s
            WHERE   user_id = %s
            """,
            (credentials, user_id),
        )
        conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update_conversation")
        print(e)
    close_connection(conn)


##### MESSAGES #####


def insert_batch(label, email_account, start_date, end_date):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            res = cursor.execute(
                """
                INSERT INTO message_batches (label, email_account, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    label,
                    email_account,
                    start_date,
                    end_date,
                ),
            )
        conn.commit()
        batch_id = cursor.lastrowid
    except Exception as e:
        print("DB error in insert_batch:", e)
        raise
    return batch_id


def insert_message(
    batch_id,
    message_date,
    message_sender,
    message_subject,
    message_body,
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            res = cursor.execute(
                """
                INSERT INTO messages (batch_id, message_date, message_sender, message_subject, message_body)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    batch_id,
                    message_date,
                    message_sender,
                    message_subject,
                    message_body,
                ),
            )
        conn.commit()
        message_id = cursor.lastrowid
    except Exception as e:
        print("DB error in insert_message:", e)
        raise
    return message_id


# get_messages_by_batch_id
def get_messages_by_batch_id(batch_id):
    query_string = """
                    SELECT *
                    FROM messages
                    WHERE batch_id = %s
                """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query_string, (batch_id,))
        rows = cur.fetchall()
    except Exception as e:
        print("db.get_messages_by_batch_id ERROR:", e)
        return {"result": "DB_CONNECTION_ERROR"}
    close_connection(conn)
    if len(rows) == 0:
        return {"result": "MESSAGES_NOT_FOUND"}
    rows[0]["result"] = "SUCCESS"
    return rows
