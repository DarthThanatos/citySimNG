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
		b1.setSizeX(50);
		b1.setSizeY(50);
		Map a = new HashMap();
		a.put("rock", 2);
		a.put("wood", 10);
		b1.setResourcesCost(a);
		
		Building b2 = new Building();
		b2.setName("shed");
		b2.setSizeX(25);
		b2.setSizeY(25);
		Map b = new HashMap();
		b.put("wood", 15);
		b2.setResourcesCost(b);
		
		Building b3 = new Building();
		b3.setName("windmill");
		b3.setSizeX(40);
		b3.setSizeY(30);
		Map c = new HashMap();
		c.put("wood", 15);
		b3.setResourcesCost(c);
		
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
		    	System.out.println("Can't afford");
		    	return false;
		    }
		}
		for(Map.Entry<String, Integer> entry : b.getResourcesCost().entrySet()) {
		    String resource = entry.getKey();
		    Integer cost = entry.getValue();
		    actualValues.put(resource, actualValues.get(resource) - cost);
		}
		return true;
	}
}
