from django.db.utils import OperationalError


def test_db_connection(connections):
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        return False
    else:
        return True