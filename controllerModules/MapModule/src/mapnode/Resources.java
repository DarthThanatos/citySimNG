package mapnode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import entities.Resource;

public class Resources {
	private List<String> resourcesNames;
	private List<Resource> resources;
	private Map<String, Integer> actualIncomes = new HashMap<String, Integer>();
	private Map<String, Integer> actualResourcesValues = new HashMap<>();
	private final String relativeTexturesPath = "resources\\Textures\\";

	public Resources(DependenciesRepresenter dr){
		actualIncomes = (Map<String, Integer>) dr.getModuleData("incomes");
		resourcesNames = (List<String>) dr.getModuleData("resourcesNames");
		resources = (List<Resource>) dr.getModuleData("resourcesList");
		for (String resourceName : resourcesNames){
			actualResourcesValues.put(resourceName, 0);
		}
		dr.setStockPile(actualResourcesValues);
	}

	public void updateResources(){
	    // update current resources values
		for(String resource : resourcesNames){
			actualResourcesValues.put(resource, actualResourcesValues.get(resource) + actualIncomes.get(resource));

			// resource amount can't be less than 0
			if(actualResourcesValues.get(resource) < 0)
				actualResourcesValues.put(resource, 0);
		}



//		JSONObject json = new JSONObject();
//		json.put("actualResourcesValues", actualResourcesValues);
//		json.put("actualIncomes", actualIncomes);
//		JSONObject envelope = new JSONObject();
//		envelope.put("To", "Map");
//		envelope.put("Operation", "Update");
//		envelope.put("Args", json);
	}

	public Map<String, Integer> getActualResourcesValues(){
		return this.actualResourcesValues;
	}

	public Map<String, Integer> getActualIncomes(){
		return this.actualIncomes;
	}

	public List<String> getResourcesNames(){
		return this.resourcesNames;
	}

	public List<Resource> getResources(){
		return this.resources;
	}


	public void setActualResourcesValues(Map<String, Integer> actualResourcesValues){
		this.actualResourcesValues = actualResourcesValues;
	}

	public void setActualIncomes(Map<String, Integer> actualIncomes){
		this.actualIncomes = actualIncomes;
	}


}
