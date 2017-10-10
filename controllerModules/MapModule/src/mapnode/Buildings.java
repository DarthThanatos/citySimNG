package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import entities.Building;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;

public class Buildings {
	private List<Building> allBuildings;
	private Map<String, Building> playerBuildings;

	public Buildings(DependenciesRepresenter dr){
		allBuildings = (List<Building>) dr.getModuleData("allBuildings");

		for(Building building: allBuildings){
			if(building.getPredecessor().equals("None"))
				building.setEnabled(true);
		}

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
	
	public PlaceBuildingResponse placeBuilding(String buildingName, String buildingId, Resources resources,
											   Dwellers dwellers){
		Building building = findBuildingWithName(buildingName);

		resources.subBuildingsCost(building);
		resources.addBuildingConsumption(building);
		resources.addBuildingsBalance(building);

		// TODO:
		//unlockSuccessors(building);
		List<String> unlockedBuildings = new ArrayList<String>();
		unlockedBuildings.add(building.getSuccessor());
		unlockedBuildings.add("Mill");

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

		return new PlaceBuildingResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getCurrDwellersAmount(),
				dwellers.getCurrDwellersMaxAmount(),
				unlockedBuildings);
	}
	
	public DeleteBuildingResponse deleteBuilding(String buildingId, Resources resources, Dwellers dwellers){
		Building building = findBuildingWithId(buildingId);

		// TODO:
//		lockSuccessors(building);
		List<String> lockedBuildings = new ArrayList<String>();
		lockedBuildings.add(building.getPredecessor());
		lockedBuildings.add("Mill");

		// if building is not running we don't have to modify incomes 
		if(!building.isRunning()){
			playerBuildings.remove(buildingId);
			return new DeleteBuildingResponse(
					resources.getActualResourcesValues(),
					resources.getActualResourcesIncomes(),
					resources.getActualResourcesConsumption(),
					resources.getResourcesBalance(),
					dwellers.getCurrDwellersAmount(),
					dwellers.getCurrDwellersMaxAmount(),
					lockedBuildings);
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
		return new DeleteBuildingResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getCurrDwellersAmount(),
				dwellers.getCurrDwellersMaxAmount(),
				lockedBuildings);
	}

	public StopProductionResponse stopProduction(String buildingId, Resources resources, Dwellers dwellers){
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

		return new StopProductionResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getCurrDwellersAmount(),
				dwellers.getCurrDwellersMaxAmount(),
				building.isRunning());
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

	private void unlockSuccessors(Building building){
		for(Building successor: allBuildings){
			if(building.getSuccessor().equals(successor.getName()))
				successor.setEnabled(true);
		}
	}

	private void lockSuccessors(Building building){
		for(String playerBuilding: playerBuildings.keySet())
			if(playerBuilding.equals(building.getName()))
				return;
		for(Building b: allBuildings){

		}
	}
	/* Getters and setters */

	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public Map<String, Building> getPlayerBuildings() {
		return playerBuildings;
	}

}
