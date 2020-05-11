import psycopg2


class DatabaseController:
    """Basic database controller class"""

    # connect to the db
    @staticmethod
    def query_tiles(query):
        con = psycopg2.connect(
            user="postgres",
            password="timetravel",
            host="127.0.0.1",
            port="5432",
            database="maps")

        # cursor
        curs = con.cursor()
        curs.execute(query)
        rows = curs.fetchall()

        for i in rows:
            print(i[0])

        curs.close()

        # close connection
        con.close()
