import mysql.connector
from mysql.connector import errorcode
from models import TaskItem
import logging as lg

FNAME = "pass.txt"
CAT_TBL = 'categories'
SUB_CAT_TBL = 'sub_categories'


def manage_connection(func):
    with open(FNAME, 'r') as file:
        lines = file.read().splitlines()

    cfg = {line.split(',')[0]: line.split(',')[1] for line in lines}

    try:
        cnx = mysql.connector.connect(**cfg)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            lg.error(err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            lg.error(err)
        else:
            lg.error(err)
        return

    cur = cnx.cursor()

    def wrapper(*args, **kwargs):
        result = None

        try:
            result = func(cur, *args, **kwargs)
        except Exception as err:
            lg.error("Error in function. ", err)
        else:
            cnx.commit()
        finally:
            cur.close()
            cnx.close()

        return result

    return wrapper


@manage_connection
def add_items_to_db(
        cur,
        cat_set: set[tuple[str, str]],
        items: list[TaskItem]
        ) -> None:
    '''
    Adds parsed items to DB. Before adding them, checks if there are new
    categories or sub-categories to add and adds them if it's needed
    '''

    QUERY_CATEGORIES = f"SELECT id, name FROM {CAT_TBL}"
    QUERY_SUB_CATEGORIES = f"SELECT id, name, category_id FROM {SUB_CAT_TBL}"

    cur.execute(QUERY_CATEGORIES)
    cats_in_db = dict(cur.fetchall())

    cur.execute(QUERY_SUB_CATEGORIES)
    sub_cats_in_db = {
        (cats_in_db[cat_id], name)
        for _, name, cat_id in cur.fetchall()
    }

    # sub-categories that don't exist in database
    sub_cats_diff = cat_set.difference(sub_cats_in_db)
    cats_to_check = {cat for cat, _ in sub_cats_diff}

    # categories that don't exist in database
    cats_diff = cats_to_check.difference(cats_in_db.values())

    if len(cats_diff) != 0:
        lg.info(f"Adding categories: {[x for x in cats_diff]}")

        values_str = ', '.join([f"(category!r)" for category in cats_diff])
        query = f"INSERT INTO {CAT_TBL} (name) VALUES {values_str}"
        cur.execute(query)

        cur.execute(QUERY_CATEGORIES)
        cats_in_db = dict(cur.fetchall())  # updating

    if len(sub_cats_diff) != 0:
        lg.info(f"Adding subcategories: {[x for x in sub_cats_diff]}")

        reversed_cats = {k: v for v, k in cats_in_db.items()}
        q = get_add_sub_categories_query(sub_cats_diff, reversed_cats)
        cur.execute(q)

    # Updating sub categories and creating a dictionary of
    # type: tuple(category_name, sub_category_name) => sub_category_id
    cur.execute(QUERY_SUB_CATEGORIES)
    categories_map = {
        (cats_in_db[cat_id], subcat_name): subcat_id
        for subcat_id, subcat_name, cat_id in cur.fetchall()
    }

    # Inserting items list to database
    TBL_NAME = "fl_items"
    cols = ', '.join(
        ('id', 'title', 'link', 'description', 'date', 'sub_category_id')
    )

    vals = str(
        [
            it.to_tuple(categories_map[(it.category, it.sub_category)])
            for it in items
        ]
    )[1:-1]

    add_items_query = f"INSERT INTO {TBL_NAME} ({cols}) VALUES {vals}"
    lg.info(f"Inserting {len(items)} new fl items")
    cur.execute(add_items_query)


def get_add_categories_query(categories: set[str]) -> str:
    columns = ('name',)
    table_name = 'categories'

    values = "('" + "'), ('".join(categories) + "')"
    columns_str = ', '.join(columns)

    q = f"INSERT INTO {table_name} ({columns_str}) VALUES {values}"
    return q


def get_add_sub_categories_query(
        sub_categories: set[tuple[str, str]],
        categories: dict[str, int]
        ) -> str:

    sub_categories = {
        (sub_cat, categories[cat])
        for cat, sub_cat in sub_categories
    }

    columns = ('name', 'category_id')
    table_name = 'sub_categories'

    values = str(sub_categories)[1:-1]
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
    pass
