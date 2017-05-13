package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import org.json.JSONObject;

import controlnode.SocketStreamSender;

public class Buildings {
	private List<Building> allBuildings;
	private SocketStreamSender sender;
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	public Buildings(SocketStreamSender sender, DependenciesRepresenter dr){
		allBuildings = (List<Building>) dr.getModuleData("allBuildings");
		this.sender = sender;
	}

	
	public boolean canAffordOnBuilding(String buildingName, Resources resources){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = null;
		
		for(Building building : allBuildings){
			if(building.getName().equals(buildingName)){
				b = building;
				break;
			}
		}
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    if(actualValues.get(resource) < cost){
		    	return false;
		    }
		}
		
		return true;
	}
	
	public void placeBuilding(String buildingName, Resources resources){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = null;
		for(Building building : allBuildings){
			if(building.getName().equals(buildingName)){
				b = building;
				break;
			}
		}
		
		Map<String, Integer> consumes = b.getConsumes();
		Map<String, Integer> produces = b.getProduces();
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
			
		    actualValues.put(resource, actualValues.get(resource) - cost);
		    incomes.put(resource, 
		    		incomes.get(resource)
		    		+ produces.get(resource) 
		    		- consumes.get(resource));
		}
	}
	
	public void deleteBuilding(String buildingName, Resources resources){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = null;
		
		for(Building building : allBuildings){
			if(building.getName().equals(buildingName)){
				b = building;
				break;
			}
		}
		
		Map<String, Integer> consumes = b.getConsumes();
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    // actualValues.put(resource, actualValues.get(resource) - cost);
		    incomes.put(resource, incomes.get(resource) - b.getProduces().get(resource) +
		    	consumes.get(resource));
		}
	}

	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public void setAllBuildings(List<Building> allBuildings) {
		this.allBuildings = allBuildings;
	}
}
