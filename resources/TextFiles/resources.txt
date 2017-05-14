package mapnode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.json.JSONObject.*;
import org.json.JSONObject;
import controlnode.SocketStreamSender;

public class Resources {
	private List<String> resourcesNames;
	private List<Resource> resources;
	private Map<String, Integer> incomes = new HashMap<String, Integer>();
	private Map<String, Integer> actualValues = new HashMap<String, Integer>();
	private SocketStreamSender sender;
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	public Resources(SocketStreamSender sender){
		Resource wood = new Resource("wood", "", "", relativeTexturesPath + "Wood.jpg");
		Resource rock = new Resource("rock", "", "", relativeTexturesPath + "Rock.png");
		Resource gold = new Resource("gold", "", "", relativeTexturesPath + "Gold.jpg");
		this.resourcesNames = new ArrayList<String>(Arrays.asList("wood", "rock", "gold"));
		this.resources = new ArrayList<Resource>();
		this.resources.add(wood);
		this.resources.add(rock);
		this.resources.add(gold);
		
		actualValues.put("wood", 0);
		actualValues.put("rock", 0);
		actualValues.put("gold", 0);
	
		incomes.put("wood", 3);
		incomes.put("rock", 2);
		incomes.put("gold", 10);
		
		this.sender = sender;
	}
	
	public void updateResources(){
		Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
		String sign = " +";
		for(String resource : resourcesNames){
			actualValues.put(resource, actualValues.get(resource) + incomes.get(resource));
			if(actualValues.get(resource) < 0)
				actualValues.put(resource, 0);
			if(incomes.get(resource) < 0)
				sign = " ";
			actualValuseAndIncomes.put(resource, actualValues.get(resource) + 
					sign + incomes.get(resource));
		}
		JSONObject json = new JSONObject(actualValuseAndIncomes);
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Map");
		envelope.put("Operation", "Update");
		envelope.put("Args", json);
		sender.pushStream(envelope.toString());
	}
	
	public Map<String, Integer> getActualValues(){
		return this.actualValues;
	}
	
	public Map<String, Integer> getIncomes(){
		return this.incomes;
	}
	
	public List<String> getResourcesNames(){
		return this.resourcesNames;
	}
	
	public List<Resource> getResources(){
		return this.resources;
	}
	
	
	public void setActualValues(Map<String, Integer> actualValues){
		this.actualValues = actualValues;
	}
	
	public void setIncomes(Map<String, Integer> incomes){
		this.incomes = incomes;
	}
	
	
}
