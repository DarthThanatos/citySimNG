package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import org.json.JSONObject;

import controlnode.SocketStreamSender;
import entities.Building;

public class Buildings {
	private List<Building> allBuildings;
	private Map<String, Building> playerBuildings;
	private SocketStreamSender sender;
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	public Buildings(SocketStreamSender sender, DependenciesRepresenter dr){
		allBuildings = (List<Building>) dr.getModuleData("allBuildings");
		playerBuildings = new HashMap();
		this.sender = sender;
	}
	
	public boolean canAffordOnBuilding(String buildingName, Resources resources){
		Map<String, Integer> actualValues = resources.getActualValues();
		Building b = findBuildingWithName(buildingName);
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    if(actualValues.get(resource) < cost){
		    	return false;
		    }
		}
		
		return true;
	}
	
	public void placeBuilding(String buildingName, String buildingId, Resources resources, Dwellers dwellers){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = findBuildingWithName(buildingName);
		
		Map<String, Integer> consumes = b.getConsumes();
		Map<String, Integer> produces = b.getProduces();
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
			
		    actualValues.put(resource, actualValues.get(resource) - cost);
		    incomes.put(resource, incomes.get(resource) 
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
		
		Building playerBuilding = new Building(b);
		playerBuilding.setId(buildingId);
		playerBuildings.put(buildingId, new Building(b));
	}
	
	public void deleteBuilding(String buildingId, Resources resources, Dwellers dwellers){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = findBuildingWithId(buildingId);
		
		// if building is not running we don't have to modify incomes 
		if(!b.isRunning()){
			playerBuildings.remove(buildingId);
			return;
		}
			
		Map<String, Integer> consumes = b.getConsumes();
		Map<String, Integer> produces = b.getProduces();
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    incomes.put(resource, incomes.get(resource) - 
		    		produces.get(resource) +
		    		consumes.get(resource));
		}
		
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
		Building b = findBuildingWithId(buildingId);
		Map<String, Integer> incomes = resources.getIncomes();
		Map<String, Integer> consumes = b.getConsumes();
		Map<String, Integer> produces = b.getProduces();
		
		if(b.isRunning()){
			for(Map.Entry<String, Integer> entry : produces.entrySet()) {
			    String resource = entry.getKey();
			    Integer prod = entry.getValue();
			    incomes.put(resource, incomes.get(resource) - prod + consumes.get(resource));
			}
			
			Map<String, Integer> tmp = new HashMap();
			tmp.put("Zbychu", 3);
			for(Map.Entry<String, Integer> entry : tmp.entrySet()){
				String dweller = entry.getKey();
				Integer amount = entry.getValue();
				dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() - amount);
			}
			
			b.setRunning(false);
		}
		
		else{
			for(Map.Entry<String, Integer> entry : produces.entrySet()) {
			    String resource = entry.getKey();
			    Integer prod = entry.getValue();
			    incomes.put(resource, incomes.get(resource) + prod - consumes.get(resource));
			}
			
			Map<String, Integer> tmp = new HashMap();
			tmp.put("Zbychu", 3);
			for(Map.Entry<String, Integer> entry : tmp.entrySet()){
				String dweller = entry.getKey();
				Integer amount = entry.getValue();
				dwellers.setCurrDwellersAmount(dwellers.getCurrDwellersAmount() + amount);
			}
			
			b.setRunning(true);
		}
	}
	
	public JSONObject getBuildingState(String buildingId){
		Building b = findBuildingWithId(buildingId);
		
		JSONObject json = new JSONObject();
		json.put("isRunning", b.isRunning());
		
		return json;
	}
	
	private Building findBuildingWithId(String buildingId){
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
