package entities;

import utils.CollectionConcatenationUtils;

import java.util.Map;

public class Building {
	private String name;
	private String predecessor;
	private String successor;
	private Map<String, Integer> produces;
	private Map<String, Integer> consumes;
	private Map<String, Integer> resourcesCost;
	private String texturePath;
	private String type;
	private String dwellersName;
	private Integer dwellersAmount;
	
	private Integer workingDwellers = 0;
	private String id;
	private boolean running = true;

	public boolean isEnabled() {
		return isEnabled;
	}

	public void setEnabled(boolean enabled) {
		isEnabled = enabled;
	}

	private boolean isEnabled = false;

	public boolean isProducing() {
		return producing;
	}

	public void setProducing(boolean producing) {
		this.producing = producing;
	}

	private boolean producing = false;
	private String description;
	
	public String getDescription(){
		return description;
	}
	
	public void setDescription(String description){
		this.description = description;
	}
	
	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}
	
	public Building(){
		
	}

	public Building(Building b){
		this.name = b.name;
		this.predecessor = b.predecessor;
		this.dwellersAmount = b.dwellersAmount;
		this.successor = b.successor;
		this.produces = b.produces;
		this.consumes = b.consumes;
		this.resourcesCost = b.resourcesCost;
		this.texturePath = b.texturePath;
		this.type = b.type;
		this.description = b.description;
		this.workingDwellers = 0;
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

	public String getTexturePath() {
		return texturePath;
	}
	
	public void setTexturePath(String texturePath) {
		this.texturePath = texturePath;
	}

	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
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

	public String getSuccessor() {
		return successor;
	}

	public void setSuccessor(String successor) {
		this.successor = successor;
	}

	public String getPredecessor() {
		return predecessor;
	}

	public void setPredecessor(String predecessor) {
		this.predecessor = predecessor;
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
	
	@Override
	public String toString(){
		return "Building name: " + name + "\n"
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
