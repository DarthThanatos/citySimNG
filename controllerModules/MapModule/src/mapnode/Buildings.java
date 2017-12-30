package mapnode;

import java.util.*;
import model.DependenciesRepresenter;
import entities.Building;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;

public class Buildings {
	public static int getScoreMultiplier() {
		return SCORE_MULTIPLIER;
	}
	private final static int SCORE_MULTIPLIER = 10;
	private String domestic = "domestic";
	private String industrial = "industrial";
	private List<Building> allBuildings;
	private Map<String, Building> domesticBuildings = new HashMap<>();
	private Map<String, Building> industrialBuildings = new HashMap<>();
	private Map<String, Building> playerIndustrialBuildings;
	private Map<String, Building> playerDomesticBuildings;
	private Map<String, Building> notFullyOccupiedBuildings;
	private Map<String, Building> unprovidedBuildings;

	public Buildings(DependenciesRepresenter dr){
		allBuildings = new ArrayList<>();

		for(Building building: (List<Building>) dr.getModuleData("allBuildings")){
			allBuildings.add(new Building(building));
		}

		for(Building building: allBuildings){
			if(building.getType().toLowerCase().equals(domestic))
				domesticBuildings.put(building.getName(), building);
			else
				industrialBuildings.put(building.getName(), building);
		}

		for(Building building: allBuildings){
			if(building.getPredecessor().equals("None"))
				building.setEnabled(true);
		}

		playerIndustrialBuildings = new LinkedHashMap<>();
		playerDomesticBuildings = new LinkedHashMap<>();
		notFullyOccupiedBuildings = new LinkedHashMap<>();
		unprovidedBuildings= new LinkedHashMap<>();
	}
	
	public boolean canAffordOnBuilding(String buildingName, Map<String, Integer> actualResourcesValues){
		Building building = findBuildingWithName(buildingName);
		assert building != null;
		Map<String, Integer> buildingCost = building.getResourcesCost();
		
		for(String resource: buildingCost.keySet()) {
			if (actualResourcesValues.get(resource) < buildingCost.get(resource)) {
				return false;
			}
		}
		return true;
	}
	
	public PlaceBuildingResponse placeBuilding(String buildingName, String buildingId, Resources resources,
										Dwellers dwellers){
		Building building = findBuildingWithName(buildingName);
		Building newBuilding = new Building(building);
		assert building != null;
		String buildingType = building.getType().toLowerCase();
		newBuilding.setId(buildingId);

		// update resources
		resources.subBuildingsCost(newBuilding);
		resources.addBuildingImpact(newBuilding, dwellers, this);

		// for domestic building if its working update not fully occupied buildings
		if(buildingType.equals(domestic) && newBuilding.isProducing()) {
			updateNotFullyOccupiedBuildings(dwellers, resources);
		}

		// for industrial building update needed dwellers
		if(buildingType.equals(industrial)){
			dwellers.setNeededDwellers(dwellers.getNeededDwellers()
					+ building.getDwellersAmount());
		}

		List<String> unlockedBuildings = unlockSuccessors(newBuilding);
		if(buildingType.equals(domestic))
			playerDomesticBuildings.put(buildingId, newBuilding);
		else
			playerIndustrialBuildings.put(buildingId, newBuilding);

		return new PlaceBuildingResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getNeededDwellers(),
				dwellers.getAvailableDwellers(),
				unlockedBuildings,
				getWorkingDwellers(newBuilding.getId()));
	}
	
	public DeleteBuildingResponse deleteBuilding(String buildingId, Resources resources,
										  Dwellers dwellers){
		Building building = findBuildingWithId(buildingId);
		assert building != null;
		String buildingType = building.getType().toLowerCase();

		resources.addResourcesFromBuildingDestruction(building);

		// if building is not running we don't have to modify anything
		if(!building.isRunning()){
			if(buildingType.equals(industrial))
				playerIndustrialBuildings.remove(buildingId);
			else
				playerDomesticBuildings.remove(buildingId);
			return new DeleteBuildingResponse(
					resources.getActualResourcesValues(),
					resources.getActualResourcesIncomes(),
					resources.getActualResourcesConsumption(),
					resources.getResourcesBalance(),
					dwellers.getNeededDwellers(),
					dwellers.getAvailableDwellers());
		}


		if(buildingType.equals(domestic) && building.isProducing()){
			dwellers.setAvailableDwellers(dwellers.getAvailableDwellers()
					- building.getDwellersAmount());
			updateWorkingBuildings(dwellers.getWorkingDwellers() - dwellers.getAvailableDwellers(), dwellers, resources);
		}

		if(buildingType.equals(industrial)){
			dwellers.setNeededDwellers(dwellers.getNeededDwellers()
					- building.getDwellersAmount());
			dwellers.setWorkingDwellers(dwellers.getWorkingDwellers()
					- building.getWorkingDwellers());
			updateNotFullyOccupiedBuildings(dwellers, resources);
		}

		// resources.subBuildingConsumption(building);
		resources.subBuildingsBalance(building);
		updateUnprovidedBuildings(resources, dwellers);

		if(buildingType.equals(industrial))
			playerIndustrialBuildings.remove(buildingId);
		else
			playerDomesticBuildings.remove(buildingId);

		return new DeleteBuildingResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getNeededDwellers(),
				dwellers.getAvailableDwellers());
	}

	public StopProductionResponse stopProduction(String buildingId, Resources resources, Dwellers dwellers){
		Building building = findBuildingWithId(buildingId);

		assert building != null;
		if(building.isRunning())
			stopProductionInBuilding(building, resources, dwellers);
		else
			resumeProductionInBuilding(building, resources, dwellers);

		return new StopProductionResponse(
				resources.getActualResourcesValues(),
				resources.getActualResourcesIncomes(),
				resources.getActualResourcesConsumption(),
				resources.getResourcesBalance(),
				dwellers.getNeededDwellers(),
				dwellers.getAvailableDwellers(),
				building.isRunning());
	}

	private void stopProductionInBuilding(Building building, Resources resources,
										  Dwellers dwellers){
		String buildingType = building.getType().toLowerCase();

		// for domestic building we have to change available dwellers and
		// update working buildings
		if(buildingType.equals(domestic) && building.isProducing()) {
			dwellers.setAvailableDwellers(dwellers.getAvailableDwellers()
					- building.getDwellersAmount());
			updateWorkingBuildings(dwellers.getWorkingDwellers() - dwellers.getAvailableDwellers(), dwellers, resources);
		}

		// update resources before setting dwellers in industrial building ->
		// its important cause we need appropriate dwellers factor
		resources.subBuildingsBalance(building);

		// setting that building is not running here is important in case
		// when building in which we are stopping production in not fully
		// occupied
		building.setRunning(false);

		// for industrial building we have to update needed and working dwellers
		// then we need to update not fully occupied
		if(buildingType.equals(industrial)){
			dwellers.setNeededDwellers(dwellers.getNeededDwellers()
					- building.getDwellersAmount());
			dwellers.setWorkingDwellers(dwellers.getWorkingDwellers()
					- building.getWorkingDwellers());
			building.setWorkingDwellers(0);
			updateNotFullyOccupiedBuildings(dwellers, resources);
		}

		// move building to the end of appropriate map
		if(buildingType.equals(domestic)) {
			playerDomesticBuildings.remove(building.getId());
			playerDomesticBuildings.put(building.getId(), building);
		}
		else{
			playerIndustrialBuildings.remove(building.getId());
			playerIndustrialBuildings.put(building.getId(), building);
		}

	}

	public void resumeProductionInBuilding(Building building, Resources resources,
											Dwellers dwellers){
		String buildingType = building.getType().toLowerCase();

		building.setRunning(true);
		resources.addBuildingImpact(building, dwellers, this);

		// for domestic building if its working update not fully occupied buildings
		if(buildingType.equals(domestic) && building.isProducing()) {
			updateNotFullyOccupiedBuildings(dwellers, resources);
		}

		// for industrial building update needed dwellers
		if(buildingType.equals(industrial)){
			dwellers.setNeededDwellers(dwellers.getNeededDwellers()
					+ building.getDwellersAmount());
		}
	}
	
	public Building findBuildingWithId(String buildingId){
		for(String id: playerIndustrialBuildings.keySet()){
			if(id.equals(buildingId)){
				return playerIndustrialBuildings.get(id);
			}
		}

		for(String id: playerDomesticBuildings.keySet()){
			if(id.equals(buildingId)){
				return playerDomesticBuildings.get(id);
			}
		}

		return null;
	}
	
	public Building findBuildingWithName(String buildingName){
		for(Building b: allBuildings){
			if(b.getName().equals(buildingName)){
				return b;
			}
		}
		return null;
	}

	public List<String> unlockSuccessors(Building predecessor){
		List<String> unlockedBuildings = new ArrayList<>();

		for(Building building: allBuildings){
			if(building.getPredecessor().equals(predecessor.getName())){
				building.setEnabled(true);
				unlockedBuildings.add(building.getName());
			}
		}

		return unlockedBuildings;
	}

	public Integer getWorkingDwellers(String buildingId){
		Building building = findBuildingWithId(buildingId);

		assert building != null;
		return building.getWorkingDwellers();
	}

	public void updateNotFullyOccupiedBuildings(Dwellers dwellers,
												 Resources resources){
		for(Building building: notFullyOccupiedBuildings.values()) {
			int idleDwellers = dwellers.getAvailableDwellers() - dwellers.getWorkingDwellers();
			// if no more idle dwellers then stop
			if (idleDwellers == 0)
				break;

			if (!building.isRunning())
				continue;

			notFullyOccupiedBuildings.remove(building.getId());
			resources.updateBuildingImpact(building, dwellers, this, true);
		}
	}

	private void updateWorkingBuildings(Integer numberOfDwellersToDelete, Dwellers dwellers,
										Resources resources){
		List<Building> playerIndustrialBuildingsList =
				new ArrayList<>(playerIndustrialBuildings.values());

		for(int i = playerIndustrialBuildingsList.size() - 1; i >= 0 &&
				numberOfDwellersToDelete > 0; i--) {
			Building building = playerIndustrialBuildingsList.get(i);
			if(!building.isRunning())
				continue;
			Integer dwellersDeletedFromBuilding = Integer.min(building.getWorkingDwellers(),
					numberOfDwellersToDelete);
			resources.updateBuildingImpact(building, dwellers, this,false);
			numberOfDwellersToDelete -= dwellersDeletedFromBuilding;
		}
	}

	private void updateUnprovidedBuildings(Resources resources, Dwellers dwellers){
		for(Building building: unprovidedBuildings.values()){
			resources.updateBuildingImpact(building, dwellers, this, true);
		}
	}

	/* Getters and setters */

	public List<Building> getAllBuildings() {
		return allBuildings;
	}

	public Map<String, Building> getPlayerIndustrialBuildings() {
		return playerIndustrialBuildings;
	}

	public Map<String, Building> getNotFullyOccupiedBuildings() {
		return notFullyOccupiedBuildings;
	}
	public void setNotFullyOccupiedBuildings(Map<String, Building> notFullyOccupiedBuildings) {
		this.notFullyOccupiedBuildings = notFullyOccupiedBuildings;
	}


	public 	Map<String, Building> getPlayerDomesticBuildings() {
		return playerDomesticBuildings;
	}

	public 	Map<String, Building> getUnprovidedBuildings() {
		return unprovidedBuildings;
	}

	public 	void setUnprovidedBuildings(Map<String, Building> unprovidedBuildings) {
		this.unprovidedBuildings = unprovidedBuildings;
	}

	public 	Map<String, Building> getDomesticBuildings() {
		return domesticBuildings;
	}

	public 	Map<String, Building> getIndustrialBuildings() {
		return industrialBuildings;
	}
}
