package corectness.checker;

import entities.Building;
import entities.Dweller;
import graph.BuildingNode;

import java.util.HashMap;
import java.util.Objects;

import graph.DwellerNode;
import graph.ResourceNode;
import model.DependenciesRepresenter;
import org.json.JSONArray;

import constants.Consts;
import utils.CollectionConcatenationUtils;

public class BuildingsChecker {

	private LvlMapper lvlMapper;
	private DependenciesRepresenter dr;

	public BuildingsChecker(DependenciesRepresenter dr){
		 lvlMapper = new LvlMapper();
		 this.dr = dr;
	}

	private void checkDwellersHaveEqLvl(HashMap<String, Integer> dwellersLvls, HashMap<String, Integer> buildingsLvls) throws CheckException {
		for(String buildingName: buildingsLvls.keySet()){
			Building building = dr.getGraphsHolder().getBuildingNode(buildingName).getBuilding();
			if(!Objects.equals(buildingsLvls.get(buildingName), dwellersLvls.get(building.getDwellersName()))){
				throw new CheckException("Dweller " + building.getDwellersName() + " cannot be in " + buildingName + " since their levels differ");
			}
		}
	}

	private void checkConsumedResourcesLowerEq(HashMap<String, Integer> resourcesLvls, HashMap<String, Integer> buildingsLvls) throws CheckException {
		for(String buildingName : buildingsLvls.keySet()){
			Building building = dr.getGraphsHolder().getBuildingNode(buildingName).getBuilding();
			if(building.getType().equals("Domestic")) continue;
			for (String consumedResource : building.getConsumes().keySet()){
				if(building.getConsumes().get(consumedResource) == 0) continue;
				if(resourcesLvls.get(consumedResource) > buildingsLvls.get(buildingName)){
					throw new CheckException("Building " + buildingName + " cannot consume " + consumedResource + " since " + consumedResource + " has bigger lvl");
				}
			}
		}

	}

	private void checkProducedResourcesLowerEq(HashMap<String, Integer> resourcesLvls, HashMap<String, Integer> buildingsLvls) throws CheckException {
		for(String buildingName : buildingsLvls.keySet()){
			Building building = dr.getGraphsHolder().getBuildingNode(buildingName).getBuilding();
			if(building.getType().equals("Domestic")) continue;
			for (String producedResource : building.getProduces().keySet()){
				if(building.getProduces().get(producedResource) == 0) continue;
				if(resourcesLvls.get(producedResource) < buildingsLvls.get(buildingName)){
					throw new CheckException("Building " + buildingName + " cannot produce " + producedResource + " since " + producedResource + " has lower level");
				}
			}
		}

	}

	private void checkBuiltResourcesLowerEq(HashMap<String, Integer> resourcesLvls, HashMap<String, Integer> buildingsLvls) throws CheckException {
		for(String buildingName : buildingsLvls.keySet()){
			Building building = dr.getGraphsHolder().getBuildingNode(buildingName).getBuilding();
			for (String buildResource : building.getConsumes().keySet()){
				if(building.getResourcesCost().get(buildResource) == 0) continue;
				if(resourcesLvls.get(buildResource) > buildingsLvls.get(buildingName)){
					throw new CheckException("Building " + buildingName + " cannot be built out of " + buildResource + " since " + buildResource + " has bigger lvl");
				}
			}
		}

	}

	private void checkPredecessorsType(BuildingNode buildingNode) throws CheckException {
		String buildingType = buildingNode.getBuilding().getType();
		for(BuildingNode childNode: ((HashMap<String, BuildingNode>) buildingNode.getChildren()).values()){
			String childType = childNode.getBuilding().getType();
			if(!buildingType.equals(childType))
				throw new CheckException("Building " + childNode.getName() + " has type : " + childType + " when its predecessor " + buildingNode.getName() + " has type " + buildingType );
			checkPredecessorsType(childNode);
		}
	}

	public void check() throws CheckException {
		lvlMapper.mapLevels(dr.getGraphsHolder().getResourcesGraphs(), dr.getGraphsHolder().getDwellersGraphs(), dr.getGraphsHolder().getBuildingsGraphs());
		HashMap<String, Integer> dwellersLvls = lvlMapper.getDwellersNodesLevels();
		HashMap<String, Integer> resourcesLvls = lvlMapper.getResourcesNodesLevels();
		HashMap<String, Integer> buildingsLvls = lvlMapper.getBuildingsNodesLevels();
		checkDwellersHaveEqLvl(dwellersLvls, buildingsLvls);
		checkConsumedResourcesLowerEq(resourcesLvls, buildingsLvls);
		checkProducedResourcesLowerEq(resourcesLvls,buildingsLvls);
		checkBuiltResourcesLowerEq(resourcesLvls,buildingsLvls);
		for(BuildingNode buildingNode : dr.getGraphsHolder().getBuildingsGraphs()) checkPredecessorsType(buildingNode);
	}

	
}
