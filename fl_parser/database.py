import mysql.connector
from mysql.connector import errorcode


def manage_connection(func):
    FNAME = "pass.txt"

    with open(FNAME, 'r') as file:
        lines = file.read().splitlines()

    cfg = {line.split(',')[0]: line.split(',')[1] for line in lines}

    try:
        cnx = mysql.connector.connect(**cfg, charset='utf8')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return

    cur = cnx.cursor()

    def wrapper(*args, **kwargs):
        result = None

        try:
            result = func(cur, *args, **kwargs)
        except Exception as err:
            print('Error in function!')
            print(err)
        finally:
            cur.close()
            cnx.close()

        return result

    return wrapper


@manage_connection
def show_categories(cur):
    cur.execute("select * from categories")
    for items in cur:
        print(items)
    return 1


if __name__ == '__main__':
    res = show_categories()
    # print(res)
