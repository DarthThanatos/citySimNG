package mapnode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import entities.Building;
import entities.Dweller;
import model.DependenciesRepresenter;


public class Dwellers {
    private final static int SCORE_MULTIPLIER = 5;
	private int neededDwellers = 0;
	private int availableDwellers = 5;
	private int workingDwellers = 0;
	private Map<String, Dweller> allDwellers;
	
	public Dwellers(DependenciesRepresenter dr){
		allDwellers = new HashMap<>();
		for(Dweller dweller: (List<Dweller>) dr.getModuleData("allDwellers")){
			allDwellers.put(dweller.getName(), dweller);
		}
	}

	public void updateDwellersWorkingInBuilding(Building building,
												Map<String, Building> notFullyOccupiedBuildings){
		Integer idleDwellers = availableDwellers - workingDwellers;

		Integer dwellersNeededToFillBuilding = building.getDwellersAmount() -
				building.getWorkingDwellers();
		Integer dwellersDesignatedToWork = Integer.min(idleDwellers,
				dwellersNeededToFillBuilding);

		building.setWorkingDwellers(building.getWorkingDwellers() +
				dwellersDesignatedToWork);
		workingDwellers += dwellersDesignatedToWork;

		if(!building.getWorkingDwellers().equals(building.getDwellersAmount()))
			notFullyOccupiedBuildings.put(building.getId(), building);

	}


	/* Getters and setters */

	public int getNeededDwellers() {
		return neededDwellers;
	}

	public void setNeededDwellers(int neededDwellers) {
		this.neededDwellers = neededDwellers;
	}

	public int getAvailableDwellers() {
		return availableDwellers;
	}

	public void setAvailableDwellers(int availableDwellers) {
		this.availableDwellers = availableDwellers;
	}

	public Map<String, Dweller> getAllDewellers() {
		return allDwellers;
	}

	public void setAllDewellers(Map<String, Dweller> allDewellers) {
		this.allDwellers = allDewellers;
	}

	public int getWorkingDwellers() {
		return workingDwellers;
	}

	public void setWorkingDwellers(int workingDwellers) {
		this.workingDwellers = workingDwellers;
	}

    public static int getScoreMultiplier() {
        return SCORE_MULTIPLIER;
    }
}
