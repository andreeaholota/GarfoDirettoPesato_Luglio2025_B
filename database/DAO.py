from database.DB_connect import DBConnect
from model.categories import Category
from model.products import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = ("SELECT * "
                 "FROM categories "
                 "WHERE category_name IS NOT NULL "
                 "ORDER BY category_name")

        cursor.execute(query)
        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllProducts(category_id):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = ("SELECT p.* "
                 "FROM products p, categories c "
                 "WHERE p.category_id = c.category_id "
                 "AND p.category_id = %s")

        cursor.execute(query, (category_id,))
        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    # Esiste arco tra due prodotti se entrambi sono stati venduti almeno una volta nel range selezionato.
    # Arco entrante mel prodotto che ha numero di vendite maggiore
    # peso = somma dei pezzi venduti dai prodotti (quantity nella tabella order_items)

    def getProductsByItems(category, d1, d2, idMap):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = ("SELECT v1.id AS id1, v2.id AS id2, "
                 "(v1.pezzi + v2.pezzi) AS weight, "
                 "v1.num_vendite AS vendite1, v2.num_vendite AS vendite2 "
                 "FROM ( SELECT p.product_id AS id, "
                 " COUNT(*) AS num_vendite, "
                 " SUM(oi.quantity) AS pezzi "
                 " FROM products p, categories c, order_items oi, orders o "
                 " WHERE p.product_id = oi.product_id "
                 " AND oi.order_id = o.order_id "
                 " AND c.category_id = p.category_id "
                 " AND p.category_id = %s "
                 " AND o.order_date BETWEEN %s AND %s "
                 " GROUP BY p.product_id "
                 " ORDER BY p.product_id) v1, "
                 "( SELECT p.product_id AS id, "
                 " COUNT(*) AS num_vendite, "
                 " SUM(oi.quantity) AS pezzi "
                 " FROM products p, categories c, order_items oi, orders o "
                 " WHERE p.product_id = oi.product_id "
                 " AND oi.order_id = o.order_id "
                 " AND c.category_id = p.category_id "
                 " AND p.category_id = %s "
                 " AND o.order_date BETWEEN %s AND %s "
                 " GROUP BY p.product_id "
                 " ORDER BY p.product_id) v2 "
                 "WHERE v1.id <> v2.id")

        cursor.execute(query, (category, d1, d2, category, d1, d2))

        for row in cursor.fetchall():
            id1 = row['id1']
            id2 = row['id2']
            weight = row['weight']
            vendite1 = row['vendite1']
            vendite2 = row['vendite2']

            if id1 >= id2:
                continue

            if vendite1 < vendite2:
                results.append((idMap[id1], idMap[id2], weight))
            elif vendite1 > vendite2:
                results.append((idMap[id2], idMap[id1], weight))
            elif vendite1 == vendite2:
                results.append((idMap[id1], idMap[id2], weight))
                results.append((idMap[id2], idMap[id1], weight))

        print(f"Risultati: {results}")

        cursor.close()
        conn.close()
        return results




