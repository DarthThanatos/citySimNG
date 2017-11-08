from py4j.java_collections import MapConverter, ListConverter


class Converter(object):

    def __init__(self, javaGateway=None):
        self.javaGateway = javaGateway

    def convertJavaMapToDict(self, map):
        if type(map) == dict: return map
        res = {}
        keys = map.keySet().toArray()
        for i in range(map.keySet().size()):
            key = keys[i]
            value = map.get(key)
            res[key] = value
        # if type(map )!= dict:  return {entry.getKey() : entry.getValue() for entry in map.entrySet() }
        # else: return map
        return res

    def convertDictToMap(self, dictToConvert):
        return MapConverter().convert(dictToConvert, self.javaGateway._gateway_client)

    def convertCollectionToList(self, collectionToConvert):
        return ListConverter().convert(collectionToConvert, self.javaGateway._gateway_client)