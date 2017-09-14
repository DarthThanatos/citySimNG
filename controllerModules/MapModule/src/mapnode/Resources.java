package mapnode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.DependenciesRepresenter;

import entities.Resource;

public class Resources {
	private List<String> resourcesNames;
	private List<Resource> resources;
	private Map<String, Integer> actualResourcesIncomes = new HashMap<String, Integer>();
	private Map<String, Integer> actualResourcesValues = new HashMap<>();

	public Resources(DependenciesRepresenter dr){
		actualResourcesIncomes = (Map<String, Integer>) dr.getModuleData("incomes");
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
			actualResourcesValues.put(resource, actualResourcesValues.get(resource) +
					actualResourcesIncomes.get(resource));

			// resource amount can't be less than 0
			if(actualResourcesValues.get(resource) < 0)
				actualResourcesValues.put(resource, 0);
		}
	}

	public Map<String, Integer> getActualResourcesValues(){
		return this.actualResourcesValues;
	}

	public Map<String, Integer> getActualResourcesIncomes(){
		return this.actualResourcesIncomes;
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

	public void setActualResourcesIncomes(Map<String, Integer> actualResourcesIncomes){
		this.actualResourcesIncomes = actualResourcesIncomes;
	}


}
