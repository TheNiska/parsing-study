import mysql.connector
from mysql.connector import errorcode


def manage_connection(func):
    FNAME = "pass.txt"

    with open(FNAME, 'r') as file:
        lines = file.read().splitlines()

    cfg = {line.split(',')[0]: line.split(',')[1] for line in lines}

    try:
        cnx = mysql.connector.connect(**cfg)
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
        else:
            cnx.commit()
            print('Done!')
        finally:
            cur.close()
            cnx.close()

        return result

    return wrapper


@manage_connection
def get_sub_categories(cur):
    cur.execute("select * from categories")
    for items in cur:
        print(items)
    return 1


@manage_connection
def add_sub_categories(cur, cat_set: set[tuple[str, str]]) -> None:
    cur.execute("SELECT * FROM categories")
    categories_in_db = dict(cur.fetchall())

    cur.execute("SELECT name, category_id FROM sub_categories")
    sub_categories_in_db = {(categories_in_db[cat_id], name)
                            for name, cat_id in cur.fetchall()}

    # sub-categories that don't exist in database
    sub_categories_diff = cat_set.difference(sub_categories_in_db)
    cats_to_check = {category for category, _ in sub_categories_diff}

    # categories that don't exist in database
    categories_diff = cats_to_check.difference(categories_in_db.values())

    if len(categories_diff) != 0:
        query = get_add_categories_query(categories_diff)
        print(query)

    if len(sub_categories_diff) != 0:



def get_add_categories_query(categories: set[str]) -> str:
    columns = ('name',)
    table_name = 'categories'

    values = "('" + "'), ('".join(categories) + "')"
    columns_str = ', '.join(columns)

    q = f"INSERT INTO {table_name} ({columns_str}) VALUES {values}"
    return q

def get_add_sub_categories_query(categories: set[str]) -> str:
    columns = ('name',)
    table_name = 'categories'

    values = "('" + "'), ('".join(categories) + "')"
    columns_str = ', '.join(columns)

    q = f"INSERT INTO {table_name} ({columns_str}) VALUES {values}"
    return q


@manage_connection
def execute_query(cur, query: str) -> None:
    print(query)
    res = cur.execute(query)
    cur.execute("select * from categories")
    for row in cur:
        print(row)


if __name__ == '__main__':
    add_sub_categories({('Разработка сайтов', 'Сайт «под ключ»')})
