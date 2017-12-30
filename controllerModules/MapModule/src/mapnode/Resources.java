package mapnode;

import java.util.*;

import entities.Building;
import entities.Dweller;
import model.DependenciesRepresenter;

import entities.Resource;
import java.util.logging.*;

public class Resources {
	public static int getScoreMultiplier() {
		return SCORE_MULTIPLIER;
	}

	private final static int SCORE_MULTIPLIER = 1;
	private Map<String, Resource> resources;
	private Map<String, Integer> basicResourcesIncomes = new HashMap<>();
	private Map<String, Integer> actualResourcesIncomes = new HashMap<>();
	private Map<String, Integer> actualResourcesConsumption = new HashMap<>();
	private Map<String, Integer> actualResourcesValues = new HashMap<>();
	private Map<String, Integer> resourcesBalance = new HashMap<>();
	private static final Logger LOGGER = Logger.getLogger(
			Resources.class.getName());

	public Resources(DependenciesRepresenter dr){
		resources = new HashMap<>();
		for(Resource resource: (List<Resource>) dr.getModuleData("resourcesList")){
			resources.put(resource.getName(), resource);
		}
		basicResourcesIncomes = (Map<String, Integer>) dr.getModuleData("incomes");
		actualResourcesIncomes = new HashMap<>(basicResourcesIncomes);
		resourcesBalance = new HashMap<>(basicResourcesIncomes);

		for (String resourceName : resources.keySet()){
			actualResourcesValues.put(resourceName, 0);
			actualResourcesConsumption.put(resourceName, 0);
		}
		dr.setStockPile(actualResourcesValues);
	}

	public void calculateCurrentCycle(Dwellers dwellers, Buildings buildings){
		LOGGER.log(Level.FINE, "Counting current cycle start ...");

		LOGGER.log(Level.FINE, "Updating current resources: {0} by income: {1}",
				new Object[]{actualResourcesValues, actualResourcesIncomes});

		// First update current resources values according to actual incomes
		for(String resource : resources.keySet()){
			actualResourcesValues.put(resource,
					actualResourcesValues.get(resource) +
							actualResourcesIncomes.get(resource));
		}

		LOGGER.log(Level.FINE, "Res values after update: {0}",
				actualResourcesValues);

		// Calculate incomes and balance for new cycle
		actualResourcesIncomes = new HashMap<>(basicResourcesIncomes);
		resourcesBalance = new HashMap<>(basicResourcesIncomes);
		actualResourcesConsumption = new HashMap<>();
		for(String resName: resources.keySet()) {
			actualResourcesConsumption.put(resName, 0);
		}
		buildings.setNotFullyOccupiedBuildings(new LinkedHashMap<>());
		buildings.setUnprovidedBuildings(new LinkedHashMap<>());
		dwellers.setAvailableDwellers(5);
		dwellers.setWorkingDwellers(0);

		LOGGER.log(Level.FINE, "Adding impact for domestic buildings");

		// First calculate impact for domestic buildings
		for(Building building: buildings.getPlayerDomesticBuildings().values())
			addBuildingImpact(building, dwellers, buildings);

		// Then calculate impact for industrial buildings
		for(Building building: buildings.getPlayerIndustrialBuildings().values())
			addBuildingImpact(building, dwellers, buildings);
	}

	public void addBuildingImpact(Building building, Dwellers dwellers,
								  Buildings buildings){
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();
		Map<String, Building> unprovidedBuildings = buildings.getUnprovidedBuildings();
		String buildingType = building.getType().toLowerCase();

		// if building is not running return
		if(!building.isRunning())
			return;

		building.setProducing(true);
		double dwellersFactor = 1.0;

		// for industrial building update working dwellers and dwellers factor
		if(!buildingType.equals("domestic")) {
			building.setWorkingDwellers(0);
			dwellers.updateDwellersWorkingInBuilding(building, buildings.getNotFullyOccupiedBuildings());
			dwellersFactor = (double) building.getWorkingDwellers() /
					building.getDwellersAmount();
			if(dwellersFactor == 0)
				building.setProducing(false);
		}

		// check if can satisfy building consumption and set producing
		for(String resource : consumes.keySet()) {
			// we should take dwellers factor in consideration here cause
			// if we don't then in some cases we will print -3 and do -2
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					+ (int)Math.ceil(dwellersFactor * consumes.get(resource)));
			resourcesBalance.put(resource, resourcesBalance.get(resource)
					- (int)Math.ceil(dwellersFactor * consumes.get(resource)));
			if (actualResourcesValues.get(resource) <
					(int)Math.ceil(dwellersFactor * consumes.get(resource))) {
				building.setProducing(false);
				unprovidedBuildings.put(building.getId(), building);
			}
		}

		if(building.isProducing()) {
			for (String resource : building.getConsumes().keySet()) {
				actualResourcesValues.put(resource, actualResourcesValues.get(resource)
						- (int)Math.ceil(dwellersFactor * consumes.get(resource)));
				actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
						+ (int)Math.floor(dwellersFactor * produces.get(resource)));
				resourcesBalance.put(resource, resourcesBalance.get(resource)
						+ (int)Math.floor(dwellersFactor * produces.get(resource)));
			}

			// For domestic buildings update available dwellers
			if(buildingType.equals("domestic")) {
				dwellers.setAvailableDwellers(dwellers.getAvailableDwellers()
						+ building.getDwellersAmount());
				building.setWorkingDwellers(building.getDwellersAmount());
			}
		}
	}

	public void updateBuildingImpact(Building building,
									 Dwellers dwellers,
									 Buildings buildings,
									 boolean updateActualResValues){

		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();

		Double dwellersFactor = (double) building.getWorkingDwellers() /
				building.getDwellersAmount();

		// rollback
		for(String resource : consumes.keySet()) {
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					- (int)Math.ceil(dwellersFactor * consumes.get(resource)));
			resourcesBalance.put(resource, resourcesBalance.get(resource)
					+ (int) Math.ceil(dwellersFactor * consumes.get(resource)));
		}

		if(building.isProducing()) {
			for (String resource : building.getConsumes().keySet()) {
				if(updateActualResValues)
					actualResourcesValues.put(resource, actualResourcesValues.get(resource)
							+ (int)Math.ceil(dwellersFactor * consumes.get(resource)));
				actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
						- (int)Math.floor(dwellersFactor * produces.get(resource)));
				resourcesBalance.put(resource, resourcesBalance.get(resource)
						- (int)Math.floor(dwellersFactor * produces.get(resource)));
			}
		}

		dwellers.setWorkingDwellers(dwellers.getWorkingDwellers()
				- building.getWorkingDwellers());

		// calculate new impact
		addBuildingImpact(building, dwellers, buildings);
	}


	public void addResourcesFromBuildingDestruction(Building building){
		Map <String, Integer> buildingResCost = building.getResourcesCost();

		for(String resourceName: buildingResCost.keySet()){
			actualResourcesValues.put(resourceName, actualResourcesValues.get(resourceName)
					+ (int)Math.floor(0.5 * buildingResCost.get(resourceName)));
		}
	}

	public void subBuildingsBalance(Building building) {
		Map<String, Integer> consumes = building.getConsumes();
		Map<String, Integer> produces = building.getProduces();

		Double dwellersFactor = (double) building.getWorkingDwellers() /
				building.getDwellersAmount();

		for (String resource : building.getResourcesCost().keySet()) {
			if (building.isProducing()) {
				actualResourcesIncomes.put(resource, actualResourcesIncomes.get(resource)
						- (int)Math.floor(dwellersFactor * produces.get(resource)));
				resourcesBalance.put(resource, resourcesBalance.get(resource)
						- (int)Math.floor(dwellersFactor * produces.get(resource)));
			}

			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					- (int)Math.ceil(dwellersFactor * consumes.get(resource)));
			resourcesBalance.put(resource, resourcesBalance.get(resource)
					+ (int)Math.ceil(dwellersFactor * consumes.get(resource)));
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

		Double dwellersFactor;
		if(building.getType().toLowerCase().equals("domestic"))
			dwellersFactor = 1.0;
		else
		  	dwellersFactor = (double) building.getWorkingDwellers() /
				building.getDwellersAmount();

		for(String resource: buildingConsumption.keySet()) {
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					+ (int)Math.ceil(dwellersFactor * buildingConsumption.get(resource)));
		}
	}

	public void subBuildingConsumption(Building building){
		Map<String, Integer> buildingConsumption = building.getConsumes();

		Double dwellersFactor;
		if(building.getType().toLowerCase().equals("domestic"))
			dwellersFactor = 1.0;
		else
			dwellersFactor = (double) building.getWorkingDwellers() /
					building.getDwellersAmount();

		for(String resource: buildingConsumption.keySet()) {
			actualResourcesConsumption.put(resource, actualResourcesConsumption.get(resource)
					- (int)Math.ceil(dwellersFactor * buildingConsumption.get(resource)));
		}
	}

	/* Getters and setters */
	public Map<String, Integer> getActualResourcesValues(){
		return this.actualResourcesValues;
	}

	public Map<String, Integer> getActualResourcesIncomes(){
		return  new HashMap<>(this.actualResourcesIncomes);
	}


	public Map<String, Resource> getResources(){
		return this.resources;
	}


	public void setActualResourcesValues(Map<String, Integer> actualResourcesValues){
		this.actualResourcesValues = actualResourcesValues;
	}

	public void setActualResourcesIncomes(Map<String, Integer> actualResourcesIncomes){
		this.actualResourcesIncomes = actualResourcesIncomes;
	}

	public Map<String, Integer> getResourcesBalance() {
		return  new HashMap<>(resourcesBalance);
	}

	public Map<String, Integer> getActualResourcesConsumption() {
		return  new HashMap<>(actualResourcesConsumption);
	}

}
