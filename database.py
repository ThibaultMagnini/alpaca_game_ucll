import psycopg2

hostname = "alpacagamedb.cda2269fchf7.eu-west-1.rds.amazonaws.com"
usernamedb = "postgres"
password = "alpacagamedb"
dbname = "alpacagamedb"


def get_alpaca_with_username(username):
    conn = psycopg2.connect(host=hostname, user=usernamedb, password=password, dbname=dbname)
    current = conn.cursor()
    current.execute("SELECT * from alpaca_customization WHERE player_name=%s", (username,))
    for id, hat, shirt, shoes, player_name in current.fetchall():
        return {"id": id, "hat": hat, "shirt": shirt, "shoes": shoes, "player_name": player_name}
    conn.close()
