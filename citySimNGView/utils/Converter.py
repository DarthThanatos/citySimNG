from py4j.java_collections import MapConverter, ListConverter

class Converter(object):

    def __init__(self, javaGateway=None):
        self.javaGateway = javaGateway

    def convertJavaMapToDict(self, map):
        if type(map )!= dict:  return {entry.getKey() : entry.getValue() for entry in map.entrySet() }
        else: return map

    def convertDictToMap(self, dictToConvert):
        return MapConverter().convert(dictToConvert, self.javaGateway._gateway_client)

    def convertCollectionToList(self, collectionToConvert):
        return ListConverter().convert(collectionToConvert, self.javaGateway._gateway_client)