from Converter import Converter
from CreatorView import Consts
from py4j.java_collections import MapConverter, ListConverter

class CreatorData(object):

    def __init__(self, javaGateway):
        self.javaGateway = javaGateway

    def receiveFromDict(self, dataDict):
        creatorData = self.javaGateway.jvm.py4jmediator.CreatorData()
        creatorData.setBuildings(self.getBuildingsList(dataDict))
        creatorData.setResources(self.getResourcesList(dataDict))
        creatorData.setDwellers(self.getDwellersList(dataDict))
        return creatorData

    def createNonSparseResourcesMap(self, map, resources):
        res_map = dict(map)
        for resource in resources:
            if resource not in res_map.keys():
                res_map[resource] = 0
        return res_map

    def mapResourcesDictToNamesList(self, resourcesDict):
        return [resource[Consts.RESOURCE_NAME] for resource in resourcesDict]

    def getDwellersList(self, dataDict):
        dwellersFromDict = dataDict[Consts.DWELLERS]
        dwellers = []
        resources = self.mapResourcesDictToNamesList(dataDict[Consts.RESOURCES])
        for dwellerFromDict in dwellersFromDict:
            dwellers.append(self.getDweller(dwellerFromDict, resources))
        return Converter(self.javaGateway).convertCollectionToList(dwellers)

    def getDweller(self, dwellerFromDict, resources):
        dweller = self.javaGateway.jvm.entities.Dweller()
        dweller.setPredecessor(dwellerFromDict[Consts.PREDECESSOR])
        dweller.setSuccessor(dwellerFromDict[Consts.SUCCESSOR])
        dweller.setDescription(dwellerFromDict[Consts.DESCRIPTION])
        dweller.setTexturePath(Consts.relative_textures_path + dwellerFromDict[Consts.TEXTURE_PATH])
        dweller.setName(dwellerFromDict[Consts.DWELLER_NAME])

        consumesMap = self.createNonSparseResourcesMap(dwellerFromDict[Consts.CONSUMES], resources)
        consumesMap = Converter(self.javaGateway).convertDictToMap(consumesMap)
        dweller.setConsumes(consumesMap)
        return dweller

    def getResourcesList(self, dataDict):
        resourcesFromDict = dataDict[Consts.RESOURCES]
        resources = []
        for resourceFromDict in resourcesFromDict:
            resources.append(self.getResource(resourceFromDict))
        return Converter(self.javaGateway).convertCollectionToList(resources)

    def getResource(self, resourceFromDict):
        resource = self.javaGateway.jvm.entities.Resource()
        resource.setPredecessor(resourceFromDict[Consts.PREDECESSOR])
        resource.setSuccessor(resourceFromDict[Consts.SUCCESSOR])
        resource.setDescription(resourceFromDict[Consts.DESCRIPTION])
        resource.setTexturePath(Consts.relative_textures_path + resourceFromDict[Consts.TEXTURE_PATH])
        resource.setName(resourceFromDict[Consts.RESOURCE_NAME])
        resource.setStartingIncome(int(resourceFromDict[Consts.START_INCOME]))
        return resource

    def getBuildingsList(self, dataDict):
        buildingsFromDict = dataDict[Consts.BUILDINGS]
        buildings = []
        resources = self.mapResourcesDictToNamesList(dataDict[Consts.RESOURCES])
        for buildingFromDict in buildingsFromDict:
            buildings.append(self.getBuilding(buildingFromDict, resources))
        return Converter(self.javaGateway).convertCollectionToList(buildings)

    def getBuilding(self, buildingFromDict, resources):
        building = self.javaGateway.jvm.entities.Building()
        building.setPredecessor(buildingFromDict[Consts.PREDECESSOR])
        building.setSuccessor(buildingFromDict[Consts.SUCCESSOR])
        building.setDescription(buildingFromDict[Consts.DESCRIPTION])

        producesMap = self.createNonSparseResourcesMap(buildingFromDict[Consts.PRODUCES],resources)
        producesMap = Converter(self.javaGateway).convertDictToMap(producesMap)
        building.setProduces(producesMap)

        consumesMap = self.createNonSparseResourcesMap(buildingFromDict[Consts.CONSUMES], resources)
        consumesMap = Converter(self.javaGateway).convertDictToMap(consumesMap)
        building.setConsumes(consumesMap)

        resourcesCost = self.createNonSparseResourcesMap(buildingFromDict[Consts.COST_IN_RESOURCES], resources)
        resourcesCost = Converter(self.javaGateway).convertDictToMap(resourcesCost)
        building.setResourcesCost(resourcesCost)

        building.setName(buildingFromDict[Consts.BUILDING_NAME])
        building.setTexturePath(Consts.relative_textures_path + buildingFromDict[Consts.TEXTURE_PATH])
        return building
