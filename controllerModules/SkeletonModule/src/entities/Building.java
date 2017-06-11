package entities;

import java.util.List;
import java.util.Map;

public class Building {
	private String name;
	private Map<String, Integer> dewellers;
	private String predecessor;
	private String successor;
	private Map<String, Integer> produces;
	private Map<String, Integer> consumes;
	private Map<String, Integer> resourcesCost;
	private String texturePath;
	private String type;
	
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

	public Map<String, Integer> getDewellers() {
		return dewellers;
	}

	public void setDewellers(Map<String, Integer> dewellers) {
		this.dewellers = dewellers;
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
	
}
