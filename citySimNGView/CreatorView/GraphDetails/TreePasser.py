class TreePasser(object):

    def jsonTreeHeight(self, lvlList):
        return (max([self.jsonTreeHeight(childDesc["Children"]) for childDesc in lvlList]) if lvlList.__len__() != 0 else 0)+ 1

    def yieldDetails(self, lvlList):
        res = {}
        for child in lvlList:
            res[child["Name"]] = child["Details"]
            res.update(self.yieldDetails(child["Children"]))
        return res

    def mountRec(self, G, lvlList):
        for childDesc in lvlList:
            self.mountTreeLvl(G, childDesc)
            self.mountRec(G, childDesc["Children"])

    def getChildrenNames(self, lvlDesc):
        return [child["Name"] for child in lvlDesc["Children"]]

    def mountTreeLvl(self, G, lvlDesc):
        currentNodeName = str(lvlDesc["Name"])
        for childName in self.getChildrenNames(lvlDesc):
            G.add_edge(currentNodeName, str(childName), size = 0.1)
        if self.getChildrenNames(lvlDesc).__len__() == 0:
            G.add_node(currentNodeName)
        G.node[currentNodeName]["image"] = lvlDesc["Texture path"]