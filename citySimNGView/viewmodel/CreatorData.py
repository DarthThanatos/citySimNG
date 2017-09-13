from CreatorView import Consts
from utils.Converter import Converter


class CreatorData(object):

    def __init__(self, javaGateway):
        self.javaGateway = javaGateway
        print "converting creator data"

    def receiveFromDict(self, dataDict):
        creatorData = self.javaGateway.jvm.py4jmediator.CreatorData()
        creatorData.setBuildings(self.getBuildingsList(dataDict))
        creatorData.setResources(self.getResourcesList(dataDict))
        creatorData.setDwellers(self.getDwellersList(dataDict))
        return creatorData

    def createNonSparseResourcesDict(self, map, resources):
        res_map = dict(map)
        for resource in resources:
            if resource not in res_map.keys():
                res_map[resource] = 0
        return res_map

    def fetchProcessedMap(self, inputDict, resources):
        nonSparseDict = self.createNonSparseResourcesDict(inputDict, resources)
        return Converter(self.javaGateway).convertDictToMap(nonSparseDict)

    def mapResourcesDictToNamesList(self, resourcesDict):
        return [resource[Consts.RESOURCE_NAME] for resource in resourcesDict]

    def getDwellersList(self, dataDict):
        dwellersFromDict = dataDict[Consts.DWELLERS]
        dwellers = []
        resources = self.mapResourcesDictToNamesList(dataDict[Consts.RESOURCES])
        for dwellerFromDict in dwellersFromDict:
            dwellers.append(self.getDweller(dwellerFromDict, resources))
        return Converter(self.javaGateway).convertCollectionToList(dwellers)

    def fillEntityWithBasicInformation(self, entity, dict_with_info, name_key):
        entity.setPredecessor(dict_with_info[Consts.PREDECESSOR])
        entity.setSuccessor(dict_with_info[Consts.SUCCESSOR])
        entity.setDescription(dict_with_info[Consts.DESCRIPTION])
        entity.setTexturePath(Consts.relative_textures_path + dict_with_info[Consts.TEXTURE_PATH])
        entity.setName(dict_with_info[name_key])

    def getDweller(self, dwellerFromDict, resources):
        dweller = self.javaGateway.jvm.entities.Dweller()
        self.fillEntityWithBasicInformation(dweller, dwellerFromDict,Consts.DWELLER_NAME)
        dweller.setConsumes(self.fetchProcessedMap(dwellerFromDict[Consts.CONSUMES], resources))
        return dweller

    def getResourcesList(self, dataDict):
        resourcesFromDict = dataDict[Consts.RESOURCES]
        resources = []
        for resourceFromDict in resourcesFromDict:
            resources.append(self.getResource(resourceFromDict))
        return Converter(self.javaGateway).convertCollectionToList(resources)

    def getResource(self, resourceFromDict):
        resource = self.javaGateway.jvm.entities.Resource()
        self.fillEntityWithBasicInformation(resource, resourceFromDict,Consts.RESOURCE_NAME)
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
        self.fillEntityWithBasicInformation(building, buildingFromDict,Consts.BUILDING_NAME)
        building.setProduces(self.fetchProcessedMap(buildingFromDict[Consts.PRODUCES], resources))
        building.setConsumes(self.fetchProcessedMap(buildingFromDict[Consts.CONSUMES], resources))
        building.setResourcesCost(self.fetchProcessedMap(buildingFromDict[Consts.COST_IN_RESOURCES], resources))
        return building