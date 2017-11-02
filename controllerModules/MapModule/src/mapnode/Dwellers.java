package mapnode;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import entities.Building;
import entities.Dweller;
import model.DependenciesRepresenter;
import utils.CollectionConcatenationUtils;

public class Dwellers {
	private int neededDwellers = 0;
	private int availableDwellers = 5;
	private int workingDwellers = 0;
	private List<Dweller> allDwellers = new ArrayList();
	private final String relativeTexturesPath = "resources\\Textures\\";
	
	Dwellers(DependenciesRepresenter dr){
		allDwellers = (List<Dweller>) dr.getModuleData("allDwellers");
		System.out.println("Dwellers: " + CollectionConcatenationUtils.listToString(allDwellers));
	}

	public void updateDwellersWorkingInBuilding(Building building,
												Buildings buildings){
		Integer idleDwellers = availableDwellers - workingDwellers;

		Integer dwellersNeededToFillBuilding = building.getDwellersAmount() -
				building.getWorkingDwellers();
		Integer dwellersDesignatedToWork = Integer.min(idleDwellers,
				dwellersNeededToFillBuilding);
		Map<String, Building> notFullyOccupiedBuildings =
				buildings.getNotFullyOccupiedBuildings();

		building.setWorkingDwellers(building.getWorkingDwellers() +
				dwellersDesignatedToWork);
		workingDwellers += dwellersDesignatedToWork;

		if(!building.getWorkingDwellers().equals(building.getDwellersAmount()))
			notFullyOccupiedBuildings.put(building.getId(), building);

	}

	/*
	Getters and setters
	 */
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

	public List<Dweller> getAllDewellers() {
		return allDwellers;
	}

	public void setAllDewellers(List<Dweller> allDewellers) {
		this.allDwellers = allDewellers;
	}


	public int getWorkingDwellers() {
		return workingDwellers;
	}

	public void setWorkingDwellers(int workingDwellers) {
		this.workingDwellers = workingDwellers;
	}
}
