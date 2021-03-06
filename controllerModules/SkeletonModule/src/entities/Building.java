package entities;

import constants.CreatorConfig;
import utils.CollectionConcatenationUtils;

import java.util.HashMap;
import java.util.Map;

public class Building extends Entity {
	private Map<String, Integer> produces;
	private Map<String, Integer> consumes;
	private Map<String, Integer> resourcesCost;
	private String type;
	private String dwellersName;
	private Integer dwellersAmount;
	private Integer workingDwellers = 0;
	private String id;
	private boolean running = true;
	private boolean isEnabled = false;
	private boolean producing = false;
	
	public Building(){
		setName("Building");
		setDwellersAmount(1);
		setDwellersName("Dweller");
		setDescription("Description");
		setType("Industrial");
		setTexturePath(CreatorConfig.TEXTURE_ONE_DEFAULT_NAME);
		workingDwellers = 0;
		setPredecessor("None");
		setSuccessor("None");
		setProduces(new HashMap<String, Integer>(){{put("Resource",1);}});
		setConsumes(new HashMap<String, Integer>(){{put("Resource",1);}});
		setResourcesCost(new HashMap<String, Integer>(){{put("Resource",1);}});

	}

	public Building(Building b){
		this.setName(b.getName());
		this.setPredecessor(b.getPredecessor());
		this.dwellersAmount = b.dwellersAmount;
		this.setSuccessor(b.getSuccessor());
		this.produces = b.produces;
		this.consumes = b.consumes;
		this.resourcesCost = b.resourcesCost;
		this.setTexturePath(b.getTexturePath());
		this.type = b.type;
		this.description = b.description;
		this.workingDwellers = 0;
		this.dwellersName = b.getDwellersName();
	}

	public Building(String name, String predecessor, String successor, int dwellersAmount, Map<String, Integer> produces,
					Map<String, Integer> consumes, Map<String, Integer> resourcesCost, String texturePath, String type,
					String description, String dwellersName){
		this.setName(name);
		this.setPredecessor(predecessor);
		this.setSuccessor(successor);
		this.setTexturePath(texturePath);
		this.dwellersAmount = dwellersAmount;
		this.produces = produces;
		this.consumes = consumes;
		this.resourcesCost = resourcesCost;
		this.type = type;
		this.description = description;
		this.dwellersName = dwellersName;
	}

	public String getDwellersName() {
		return dwellersName;
	}

	public void setDwellersName(String dwellersName) {
		this.dwellersName = dwellersName;
	}

	public Integer getDwellersAmount() {
		return dwellersAmount;
	}

	public void setDwellersAmount(Integer dwellersAmount) {
		this.dwellersAmount = dwellersAmount;
	}

	public Map<String, Integer> getResourcesCost() {
		return resourcesCost;
	}

	public void setResourcesCost(Map<String, Integer> resourcesCost) {
		this.resourcesCost = resourcesCost;
	}

	public Map<String, Integer> getProduces() {
		return produces;
	}

	public void setProduces(Map<String, Integer> produces) {
		this.produces = produces;
	}

	public Map<String, Integer> getConsumes() {
		return consumes;
	}

	public void setConsumes(Map<String, Integer> consumes) {
		this.consumes = consumes;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public Integer getWorkingDwellers() {
		return workingDwellers;
	}

	public void setWorkingDwellers(Integer workingDwellers) {
		this.workingDwellers = workingDwellers;
	}

	public boolean isRunning() {
		return running;
	}

	public void setRunning(boolean running) {
		this.running = running;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public boolean isProducing() {
		return producing;
	}

	public void setProducing(boolean producing) {
		this.producing = producing;
	}

	public boolean isEnabled() {
		return isEnabled;
	}

	public void setEnabled(boolean enabled) {
		isEnabled = enabled;
	}

	@Override
	public String toString(){
		return "Building name: " + getName() + "\n"
				+ "\n=====================\n"
				+ "Type: " + type + "\n"
				+ "\n=====================\n"
				+ "Dweller living here: " + dwellersName + "\n"
				+ "\n=====================\n"
				+ "Produces: \n" + CollectionConcatenationUtils.filteredMapToString(produces)
				+ "\n=====================\n"
				+ "Consumes: \n" + CollectionConcatenationUtils.filteredMapToString(consumes)
				+ "\n=====================\n"
				+ "Cost in resources: \n" + CollectionConcatenationUtils.filteredMapToString(resourcesCost);
				
	} 
	

}
