package mapnode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import entities.Building;
import model.DependenciesRepresenter;

import entities.Resource;

public class Resources {
	private List<Resource> resources;
	private List<String> resourcesNames;
	private Map<String, Integer> basicResourcesIncomes = new HashMap<>();
	private Map<String, Integer> actualResourcesIncomes = new HashMap<>();
	private Map<String, Integer> actualResourcesConsumption = new HashMap<>();
	private Map<String, Integer> actualResourcesValues = new HashMap<>();
	private Map<String, Integer> resourcesBalance = new HashMap<>();

	public Resources(DependenciesRepresenter dr){
		resources = (List<Resource>) dr.getModuleData("resourcesList");
		resourcesNames = (List<String>) dr.getModuleData("resourcesNames");
		basicResourcesIncomes = (Map<String, Integer>) dr.getModuleData("incomes");
		actualResourcesIncomes = new HashMap<>(basicResourcesIncomes);
		resourcesBalance = new HashMap<>(basicResourcesIncomes);

		for (String resourceName : resourcesNames){
			actualResourcesValues.put(resourceName, 0);
			actualResourcesConsumption.put(resourceName, 0);
		}
		dr.setStockPile(actualResourcesValues);
	}

	public void updateResources(Map<String, Building> playerBuildings){
	    // update current resources values
		for(String resource : resourcesNames){
			actualResourcesValues.put(resource, actualResourcesValues.get(resource)
					+ actualResourcesIncomes.get(resource));
		}

		// calculate income and balance
		actualResourcesIncomes = new HashMap<>(basicResourcesIncomes);
		resourcesBalance = new HashMap<>(basicResourcesIncomes);

		for(Building building: playerBuildings.values())
			addBuildingsBalance(building);
	}

	public void addBuildingsBalance(Building building){
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();

		building.setProducing(true);

		// if player hasn't got enough resources building won't produce anything
		for(String resource : consumes.keySet()) {
			resourcesBalance.put(resource, resourcesBalance.get(resource)
					- consumes.get(resource));
			if (actualResourcesValues.get(resource) < consumes.get(resource))
				building.setProducing(false);
		}

		if(building.isProducing()) {
			for (String resource : building.getConsumes().keySet()) {
				actualResourcesValues.put(resource, actualResourcesValues.get(resource)
						- consumes.get(resource));
				actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
						+ produces.get(resource));
				resourcesBalance.put(resource, resourcesBalance.get(resource)
						+ produces.get(resource));
			}
		}
	}

	public void subBuildingsBalance(Building building) {
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();

		for (String resource : building.getResourcesCost().keySet()) {
			if (building.isProducing())
				actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
						- produces.get(resource));

			resourcesBalance.put(resource, resourcesBalance.get(resource)
					+ consumes.get(resource));
		}
	}

	public void subBuildingsCost(Building building){
		Map<String, Integer> buildingCost = building.getResourcesCost();

		for(String resource: buildingCost.keySet()) {
			actualResourcesValues.put(resource, actualResourcesValues.get(resource)
					- buildingCost.get(resource));
		}
	}

	public void addBuildingConsumption(Building building){
		Map<String, Integer> buildingConsumption = building.getConsumes();

		for(String resource: buildingConsumption.keySet()) {
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					+ buildingConsumption.get(resource));
		}
	}

	public void subBuildingConsumption(Building building){
		Map<String, Integer> buildingConsumption = building.getConsumes();

		for(String resource: buildingConsumption.keySet()) {
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					- buildingConsumption.get(resource));
		}
	}
	/* Getters and setters */
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

	public Map<String, Integer> getResourcesBalance() {
		return resourcesBalance;
	}

	public Map<String, Integer> getActualResourcesConsumption() {
		return actualResourcesConsumption;
	}

}
