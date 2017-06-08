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
	
	public void placeBuilding(String buildingName, String buildingId, Resources resources, Dwellers dwellers){
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

	public void stopProduction(String buildingId, Resources resources){
		Building b = null;
		Map<String, Integer> incomes = resources.getIncomes();
		
		for(String id: playerBuildings.keySet()){
			if(id.equals(buildingId)){
				b = playerBuildings.get(id);
				if(b.isRunning())
					b.setRunning(false);
				else
					b.setRunning(true);
				break;
			}
		}

		for(Map.Entry<String, Integer> entry : b.getProduces().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    // actualValues.put(resource, actualValues.get(resource) - cost);
		    if(!b.isRunning())
		    	incomes.put(resource, incomes.get(resource) - b.getProduces().get(resource));
		    else
		    	incomes.put(resource, incomes.get(resource) + b.getProduces().get(resource));
		}
		
		
	}
	
	public JSONObject getBuildingState(String buildingId){
		Building b = null;
		
		for(String id: playerBuildings.keySet()){
			if(id.equals(buildingId)){
				b = playerBuildings.get(id);
				break;
			}
		}
		
		JSONObject json = new JSONObject();
		json.put("isRunning", b.isRunning());
		return json;
	}
	
	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public void setAllBuildings(List<Building> allBuildings) {
		this.allBuildings = allBuildings;
	}
}
