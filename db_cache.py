import sqlite3

conn = sqlite3.connect("weight.db")
cursor = conn.cursor()

def memoize_weight_with_db(weight_func):
    def decorated(board):
        h = board.hashstr()
        cursor.execute("SELECT value FROM weight WHERE hash = '{}' LIMIT 1".format(h))
        try:
            value = cursor.fetchall()[0][0]
        except IndexError:
            value = weight_func(board)
            cursor.execute("INSERT INTO weight values ('{}', {})".format(h, value))
            conn.commit()
        return value
    return decorated

if __name__ == "__main__":
    cursor.execute("CREATE TABLE weight (hash TEXT UNIQUE, value REAL)")
    cursor.execute("CREATE INDEX hash_index ON weight(hash)")
    
