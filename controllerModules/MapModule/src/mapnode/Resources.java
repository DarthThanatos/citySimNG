package mapnode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import org.json.JSONObject.*;
import org.json.JSONObject;

import controlnode.SocketStreamSender;
import entities.Resource;

public class Resources {
	private List<String> resourcesNames;
	private List<Resource> resources;
	private Map<String, Integer> incomes = new HashMap<String, Integer>();
	private Map<String, Integer> actualValues = new HashMap<String, Integer>();
	private SocketStreamSender sender;
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	public Resources(SocketStreamSender sender, DependenciesRepresenter dr){
		incomes = (Map<String, Integer>) dr.getModuleData("incomes");
		resourcesNames = (List<String>) dr.getModuleData("resourcesNames");
		resources = (List<Resource>) dr.getModuleData("resourcesList");
		for (String resourceName : resourcesNames){
			actualValues.put(resourceName, 0);
		}			
		dr.setStockPile(actualValues);
		this.sender = sender;
	}
	
	public SocketStreamSender getSender() {
		return sender;
	}

	public void setSender(SocketStreamSender sender) {
		this.sender = sender;
	}

	public void updateResources(){
		Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
		for(String resource : resourcesNames){
			String sign = " +";
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
