from database.DB_connect import DBConnect
from model.avvistamenti import Avvistamenti
from model.stati import Stato
from model.connessione import Connessione


class DAO:

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select * 
                from state s
                """
        cursor.execute(query)
        for row in cursor:
            result.append(Stato(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct year(s.`datetime`) as year, count(s.`datetime`) as n  
                from sighting s
                where s.country = 'us'
                group by year(s.`datetime`)
                order by s.`datetime` asc
                """
        cursor.execute(query)
        for row in cursor:
            result.append(Avvistamenti(row['year'], row['n']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStates(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select s2.*  
                from sighting s, state s2 
                where s.country = 'us'
                and year(s.`datetime`) = %s
                and s.state = s2.id 
                group by s2.id 
                having count(s.`datetime`) > 0
                """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Stato(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnections(idMap, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct p1.id as st1, p2.id as st2
                from sighting s1, sighting s2, state p1, state p2
                where s1.country = 'us'
                and s1.country = s2.country 
                and year(s1.`datetime`) = %s
                and year(s1.`datetime`) = year(s2.`datetime`)
                and s2.state = p2.id  
                and s1.state = p1.id
                and s1.`datetime` > s2.`datetime`
                and p1.id != p2.id
                """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Connessione(idMap[row['st1']], idMap[row['st2']]))
        cursor.close()
        conn.close()
        return result
