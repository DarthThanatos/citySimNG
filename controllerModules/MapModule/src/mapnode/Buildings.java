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
		
		for(Map.Entry<String, Integer> entry : building.getResourcesCost().entrySet()) {
			String resource = entry.getKey();
			Integer cost = entry.getValue();
			if (actualResourcesValues.get(resource) < cost) {
				return false;
			}
		}
		return true;
	}
	
	public void placeBuilding(String buildingName, String buildingId, Resources resources, Dwellers dwellers){
		Map<String, Integer> actualResourcesValues = resources.getActualResourcesValues();
		Map<String, Integer> actualResourcesIncomes = resources.getActualResourcesIncomes();
		Building building = findBuildingWithName(buildingName);
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();
		
		for(Map.Entry<String, Integer> entry : building.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
			
		    actualResourcesValues.put(resource, actualResourcesValues.get(resource) - cost);
		    actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
		    		+ produces.get(resource) 
		    		- consumes.get(resource));
		}
		
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
//		if(building == null)
//			return;
		Map<String, Integer> actualResourcesValues = resources.getActualResourcesValues();
		Map<String, Integer> actualResourcesIncomes = resources.getActualResourcesIncomes();
		
		// if building is not running we don't have to modify incomes 
		if(!building.isRunning()){
			playerBuildings.remove(buildingId);
			return;
		}
			
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();
		
		for(Map.Entry<String, Integer> entry : building.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource) -
		    		produces.get(resource) +
		    		consumes.get(resource));
		}

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
//		if(b == null)
//			return;
		Map<String, Integer> incomes = resources.getActualResourcesIncomes();
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();
		
		if(building.isRunning()){
			for(Map.Entry<String, Integer> entry : produces.entrySet()) {
			    String resource = entry.getKey();
			    incomes.put(resource, incomes.get(resource) - produces.get(resource) + consumes.get(resource));
			}
			
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
			for(Map.Entry<String, Integer> entry : produces.entrySet()) {
			    String resource = entry.getKey();
			    incomes.put(resource, incomes.get(resource) + produces.get(resource) - consumes.get(resource));
			}
			
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
	
	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public void setAllBuildings(List<Building> allBuildings) {
		this.allBuildings = allBuildings;
	}
}
