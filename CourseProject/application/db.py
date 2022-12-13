from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from Levenshtein import distance

db = None


def init_db():
    global db 
    db = GraphDatabase.driver('bolt://localhost:7687', auth=("neo4j", "admin"))

def get_db():
    return db

def get_all_nodes():
    result = []

    with db.session() as session:
        query_result = session.run("MATCH (n) RETURN n")

        for record in query_result:
            node = record.value()
            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result

def ngram(one, another):
    gram_len = 5

    one_trigram = [one[i:i + gram_len] for i in range(len(one) - (gram_len - 1))]
    another_trigram = [another[i:i + gram_len] for i in range(len(another) - (gram_len - 1))]

    intersect = len(set(one_trigram) & set(another_trigram))
    union = len(set(one_trigram) | set(another_trigram))

    coeff = len(one) / len(another)

    if (coeff < 1):
        coeff = 1 / coeff

    return intersect / union * coeff

def get_all_nodes_by_name(name):
    result = []

    with db.session() as session:
        query_result = session.run("MATCH (n) RETURN n")

        for record in query_result:
            node = record.value()

            # name_distance = 5
            # for name_word in name.split(' '):
            #     for word in node.get('name').split(' '):
            #         name_distance = min(name_distance, distance(name_word, word))


            # if (name_distance > 3):
            #     continue

            name_distance = ngram(name, node.get('name')) * 100

            if (name_distance < 10):
                continue

            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result


def get_all_nodes_by_name_and_description(name):
    result = []

    with db.session() as session:
        query_result = session.run("MATCH (n) RETURN n")

        for record in query_result:
            node = record.value()
            description = node.get('description')

            # name_distance = 5
            # for name_word in name.split(' '):
            #     for word in node.get('name').split(' '):
            #         name_distance = min(name_distance, distance(name_word, word))

            # description_distance = 5    
            # if description is not None:
            #     for name_word in name.split(' '):
            #         for word in description.split(' '):
            #             description_distance = min(description_distance, distance(word, name_word))

            name_distance = ngram(name, node.get('name')) * 100
            description_distance = ngram(name, description) * 100

            if (name_distance < 10 and description_distance < 10):
                continue

            # if (name_distance > 3 and description_distance > 2):
            #     continue

            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result


def get_discipline_nodes_by_name(name, disciplines):
    result = []

    with db.session() as session:
        query_result = session.run("""
                                    UNWIND $disciplines as d_name
                                    MATCH (d:discipline) - [*] -> (n) 
                                    WHERE d.name = d_name
                                    RETURN n
                                    """, disciplines=disciplines)

        for record in query_result:
            node = record.value()

            # name_distance = 5
            # for name_word in name.split(' '):
            #     for word in node.get('name').split(' '):
            #         name_distance = min(name_distance, distance(name_word, word))

            # if (name_distance > 3):
            #     continue

            name_distance = ngram(name, node.get('name')) * 100

            if (name_distance < 10):
                continue

            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result


def get_discipline_nodes_by_name_and_description(name, disciplines):
    result = []

    with db.session() as session:
        query_result = session.run("""
                                    UNWIND $disciplines as d_name
                                    MATCH (d:discipline) - [*] -> (n) 
                                    WHERE d.name = d_name
                                    RETURN n
                                    """, disciplines=disciplines)

        for record in query_result:
            node = record.value()
            description = node.get('description')

            name_distance = ngram(name, node.get('name')) * 100
            description_distance = ngram(name, description) * 100

            # name_distance = 5
            # for name_word in name.split(' '):
            #     for word in node.get('name').split(' '):
            #         name_distance = min(name_distance, distance(name_word, word))

            # description_distance = 5
            # if description is not None:
            #     for name_word in name.split(' '):
            #         for word in description.split(' '):
            #             description_distance = min(description_distance, distance(word, name_word))

            if (name_distance < 10 and description_distance < 10):
                continue

            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result


def get_by_id(id):
    with get_db().session() as session:
        record = session.run("""
                                MATCH (n)
                                WHERE ID(n) = $id
                                OPTIONAL MATCH (d:discipline) - [*] -> (n)
                                RETURN ID(n), n.name, n.description, ID(d), d.name
                             """,
                             
                              id=int(id))
        record = record.values()[0]

        return {'id': record[0], 'name': record[1], 'desc': record[2], 'did': record[3], 'dname': record[4]}


def get_all_disciplines():
    result = []

    with db.session() as session:
        query_result = session.run("MATCH (d:discipline) RETURN d")

        for record in query_result:
            node = record.value()
            result.append({'id': node.id, 'name': node.get('name'), 'desc': node.get('description')})

    return result

def close_db():
    if db is not None:
        db.close()