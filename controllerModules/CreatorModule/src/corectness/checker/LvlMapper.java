package corectness.checker;

import graph.BuildingNode;
import graph.DwellerNode;
import graph.ResourceNode;
import org.json.JSONArray;

import java.util.HashMap;
import java.util.List;

class LvlMapper{


    private HashMap<String, Integer> resourcesNodesLevels;
    private HashMap<String, Integer> dwellersNodesLevels;
    private HashMap<String, Integer> buildingsNodesLevels;

    HashMap<String, Integer> getDwellersNodesLevels() {
        return dwellersNodesLevels;
    }

    HashMap<String, Integer> getResourcesNodesLevels() {
        return resourcesNodesLevels;
    }

    HashMap<String, Integer> getBuildingsNodesLevels(){
        return buildingsNodesLevels;
    }

    private void mapLevelsToRNL(ResourceNode resourceNode, int lvl){
        resourcesNodesLevels.put(resourceNode.getName(), lvl);
        for(ResourceNode childNode : ((HashMap<String, ResourceNode>)resourceNode.getChildren()).values()){
            mapLevelsToRNL(childNode, lvl +1 );
        }
    }

    private void mapLevelsToDNL(DwellerNode dwellerNode, int lvl){
        dwellersNodesLevels.put(dwellerNode.getName(), lvl);
        for(DwellerNode childNode : ((HashMap<String, DwellerNode>) dwellerNode.getChildren()).values()){
            mapLevelsToDNL(childNode, lvl+1);
        }
    }

    private void mapLevelsToBNL(BuildingNode buildingNode, int lvl){
        buildingsNodesLevels.put(buildingNode.getName(), lvl);
        for(BuildingNode childNode: ((HashMap<String, BuildingNode>) buildingNode.getChildren()).values()){
            mapLevelsToBNL(childNode, lvl + 1);
        }
    }

    private void mapResourcesLevels(List resourcesRoots){
        resourcesNodesLevels = new HashMap<>();
        for(ResourceNode resourceNode: (List<ResourceNode>)resourcesRoots){
            mapLevelsToRNL(resourceNode, 0);
        }
    }

    private void mapDwellersLevels(List dwellersRoots){
        dwellersNodesLevels = new HashMap<>();
        for(DwellerNode dwellerNode : (List<DwellerNode>)dwellersRoots){
            mapLevelsToDNL(dwellerNode, 0);
        }
    }


    private void mapBuildingsLevels(List buildingsRoots){
        buildingsNodesLevels = new HashMap<>();
        for(BuildingNode buildingNode : (List<BuildingNode>)buildingsRoots){
            mapLevelsToBNL(buildingNode, 0);
        }

    }

    void mapLevels(List resourcesRoots, List dwellersRoots){
        mapResourcesLevels(resourcesRoots);
        mapDwellersLevels(dwellersRoots);
    }

    void mapLevels(List resourcesRoots, List dwellersRoots, List buildingsRoots){
        mapResourcesLevels(resourcesRoots);
        mapDwellersLevels(dwellersRoots);
        mapBuildingsLevels(buildingsRoots);
    }
}
