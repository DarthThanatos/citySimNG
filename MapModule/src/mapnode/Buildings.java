package mapnode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONObject;

import controlnode.SocketStreamSender;

public class Buildings {
	private List<Building> allBuildings;
	private SocketStreamSender sender;
	
	public Buildings(SocketStreamSender sender){
		allBuildings = new ArrayList<Building>();
		Building b1 = new Building();
		b1.setName("house");
		b1.setTexture("Textures\\Building1.png");
		Map a = new HashMap();
		a.put("rock", 2);
		a.put("wood", 10);
		b1.setResourcesCost(a);
		Map a2 = new HashMap();
		a2.put("rock", 1);
		a2.put("wood", 3);
		b1.setProduces(a2);
		
		Building b2 = new Building();
		b2.setName("shed");
		b2.setTexture("Textures\\Building.png");
		Map b = new HashMap();
		b.put("wood", 15);
		b2.setResourcesCost(b);
		Map bm2 = new HashMap();
		bm2.put("rock", 1);
		bm2.put("wood", 3);
		b2.setProduces(bm2);
		
		
		Building b3 = new Building();
		b3.setName("windmill");
		b3.setTexture("Textures\\Building3.png");
		Map c = new HashMap();
		c.put("wood", 15);
		b3.setResourcesCost(c);
		Map c2 = new HashMap();
		c2.put("rock", 1);
		c2.put("wood", 3);
		b3.setProduces(c2);
		
		allBuildings.add(b1);
		allBuildings.add(b2);
		allBuildings.add(b3);
		
		this.sender = sender;
	}
	
	public void sendBuildingsInfo(){
		JSONObject json = new JSONObject();
		json.put("Buildings", allBuildings);
		System.out.println(json);
		synchronized(sender){
		sender.setStream("Map@" + json);
		sender.notify();
		} 
	}
	
	public boolean placeBuilding(String buildingsName, Resources resources){
		Map<String, Integer> actualValues = resources.getActualValues();
		Map<String, Integer> incomes = resources.getIncomes();
		Building b = null;
		
		for(Building building : allBuildings){
			if(building.getName().equals(buildingsName)){
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
		
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    actualValues.put(resource, actualValues.get(resource) - cost);
		    incomes.put(resource, incomes.get(resource) + b.getProduces().get(resource));
		}
		
		
		
		return true;
	}
}
