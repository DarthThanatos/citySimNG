package mapnode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import entities.Building;

public class Buildings {
	private List<Building> allBuildings;
	private Map<String, Building> playerBuildings;

	public Buildings(DependenciesRepresenter dr){
		allBuildings = (List<Building>) dr.getModuleData("allBuildings");
		playerBuildings = new HashMap<>();
	}
	
	public boolean canAffordOnBuilding(String buildingName, Map<String, Integer> actualResourcesValues){
		Building building = findBuildingWithName(buildingName);
		Map<String, Integer> buildingCost = building.getResourcesCost();
		
		for(String resource: buildingCost.keySet()) {
			if (actualResourcesValues.get(resource) < buildingCost.get(resource)) {
				return false;
			}
		}
		return true;
	}
	
	public void placeBuilding(String buildingName, String buildingId, Resources resources, Dwellers dwellers){
		Building building = findBuildingWithName(buildingName);

		resources.subBuildingsCost(building);
		resources.addBuildingConsumption(building);
		resources.addBuildingsBalance(building);
		
		// TODO get this map from dwellers when they will work in creator
		Map<String, Integer> tmp = new HashMap();
		tmp.put("Zbychu", 3);
		for(Map.Entry<String, Integer> entry : tmp.entrySet()){
			String dweller = entry.getKey();
			Integer amount = entry.getValue();
			dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() + amount);
		}
		
		Building newBuilding = new Building(building);
		newBuilding.setId(buildingId);
		playerBuildings.put(buildingId, newBuilding);
	}
	
	public void deleteBuilding(String buildingId, Resources resources, Dwellers dwellers){
		Building building = findBuildingWithId(buildingId);

		// if building is not running we don't have to modify incomes 
		if(!building.isRunning()){
			playerBuildings.remove(buildingId);
			return;
		}

		resources.subBuildingConsumption(building);
		resources.subBuildingsBalance(building);

		// TODO:
		Map<String, Integer> tmp = new HashMap();
		tmp.put("Zbychu", 3);
		for(Map.Entry<String, Integer> entry : tmp.entrySet()){
			String dweller = entry.getKey();
			Integer amount = entry.getValue();
			dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() - amount);
		}
		
		playerBuildings.remove(buildingId);
	}

	public void stopProduction(String buildingId, Resources resources, Dwellers dwellers){
		Building building = findBuildingWithId(buildingId);

		if(building.isRunning()){
			resources.subBuildingConsumption(building);
			resources.subBuildingsBalance(building);
			
			Map<String, Integer> tmp = new HashMap();
			tmp.put("Zbychu", 3);
			for(Map.Entry<String, Integer> entry : tmp.entrySet()){
				String dweller = entry.getKey();
				Integer amount = entry.getValue();
				dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() - amount);
			}
			
			building.setRunning(false);
		}
		
		else{
			resources.addBuildingConsumption(building);
			resources.addBuildingsBalance(building);

			Map<String, Integer> tmp = new HashMap();
			tmp.put("Zbychu", 3);
			for(Map.Entry<String, Integer> entry : tmp.entrySet()){
				String dweller = entry.getKey();
				Integer amount = entry.getValue();
				dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() + amount);
			}
			
			building.setRunning(true);
		}
	}
	
	public Building findBuildingWithId(String buildingId){
		for(String id: playerBuildings.keySet()){
			if(id.equals(buildingId)){
				return playerBuildings.get(id);
			}
		}
		return null;
	}
	
	private Building findBuildingWithName(String buildingName){
		for(Building b: allBuildings){
			if(b.getName().equals(buildingName)){
				return b;
			}
		}
		return null;
	}

	/* Getters and setters */

	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public Map<String, Building> getPlayerBuildings() {
		return playerBuildings;
	}

}
