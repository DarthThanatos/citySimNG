from CreatorView import Consts


class RedundancyChecker(object):

    def newResultStruct(self):
        return {"ErrorMsg":"Delete operation not successful:\n"} # init error msg displayed if sth went wrong

    def __init__(self, creator_main_panel):
        self.creator_main_panel = creator_main_panel

    def checkIfRedundant(self, entity, result_struct):
        raise Exception("checkIfRedundant not implemented")

    def checkInnerSetRelationshipNotExist(self, entityName, entityType, relationshipKey):
        # e.g. relationship between Resources, like one resource is the predecessor of another resource(note the same set)
        entities = self.creator_main_panel.current_dependencies[entityType]
        for otherEntity in entities.keys():
            if entityName != otherEntity and entities[otherEntity][relationshipKey] == entityName:
                return False,otherEntity
        return True,None

class ResourceRedundancyChecker(RedundancyChecker):

    def checkBetweenSetRelationshipNotExist(self, resourceName, otherSet, relationshipKey):
        otherSetObjs = self.creator_main_panel.current_dependencies[otherSet]
        for otherSetObj in otherSetObjs:
            if resourceName in otherSetObjs[otherSetObj][relationshipKey].keys():
                return False,otherSetObj
        return True,None

    def checkResourceIsNoPredecessor(self, entity, result_struct):
        no_relationship, what = self.checkInnerSetRelationshipNotExist(entity, Consts.RESOURCES, Consts.PREDECESSOR)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + entity + " is a predecessor of " + what + "\n"
            return False
        return True

    def checkResourceIsNotProducedByBuildings(self, entity, result_struct):
        no_relationship, what = self.checkBetweenSetRelationshipNotExist(entity, Consts.BUILDINGS, Consts.PRODUCES)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + entity + " is produced by " + what + "\n"
            return False
        return True

    def checkResourceNotCostBuildings(self, entity, result_struct):
        no_relationship, what = self.checkBetweenSetRelationshipNotExist(entity,Consts.BUILDINGS, Consts.COST_IN_RESOURCES)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + entity + " is necessary for " + what + " to be built\n"
            return False
        return True

    def checkResourceIsNotConsumedByBuildings(self, entity, result_struct):
        no_relationship, what = self.checkBetweenSetRelationshipNotExist(entity, Consts.BUILDINGS, Consts.CONSUMES)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + entity + " is necessary for " + what + " to produce goods\n"
            return False
        return True

    def checkResourceIsNotConsumedByDwellers(self, entity, result_struct):
        no_relationship, what = self.checkBetweenSetRelationshipNotExist(entity, Consts.DWELLERS, Consts.CONSUMES)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + entity + " is consumed by " + what + "\n"
            return False
        return True

    def checkIfRedundant(self, entity, result_struct):
        redundant = self.checkResourceIsNoPredecessor(entity, result_struct)
        redundant &= self.checkResourceIsNotProducedByBuildings(entity, result_struct)
        redundant &= self.checkResourceNotCostBuildings(entity, result_struct)
        redundant &= self.checkResourceIsNotConsumedByBuildings(entity, result_struct)
        redundant &= self.checkResourceIsNotConsumedByDwellers(entity, result_struct)
        return redundant

class BuildingRedundancyChecker(RedundancyChecker):

    def checkIfBuildingIsNoPredecessor(self, building, result_struct):
        no_relationship, what = self.checkInnerSetRelationshipNotExist(building, Consts.BUILDINGS, Consts.PREDECESSOR)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + building + " is a predecessor of " + what + "\n"
            return False
        return True

    def checkIfRedundant(self, entity, result_struct):
        return self.checkIfBuildingIsNoPredecessor(entity, result_struct)

class DwellerRedundancyChecker(RedundancyChecker):

    def checkIfDwellerIsNoPredecessor(self, dweller, result_struct):
        no_relationship, what = self.checkInnerSetRelationshipNotExist(dweller, Consts.DWELLERS, Consts.PREDECESSOR)
        if not no_relationship:
            result_struct["ErrorMsg"] += "-> " + dweller + " is a predecessor of " + what + "\n"
            return False
        return True

    def checkIfDwellerHasNoBuilding(self, dwellerName, result_struct):
        buildings = self.creator_main_panel.current_dependencies[Consts.BUILDINGS]
        for building in buildings.values():
            if dwellerName == building[Consts.DWELLER_NAME]:
                result_struct["ErrorMsg"] += "-> " + dwellerName + " lives in " + building[Consts.BUILDING_NAME] + "\n"
                return False
        return True

    def checkIfRedundant(self, entity, result_struct):
        redundant = self.checkIfDwellerIsNoPredecessor(entity, result_struct)
        redundant &= self.checkIfDwellerHasNoBuilding(entity, result_struct)
        return redundant
