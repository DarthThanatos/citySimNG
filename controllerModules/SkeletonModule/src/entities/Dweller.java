package entities;

import java.util.Map;

public class Dweller {
	private String name;
	private String predecessor;
	private String successor;
	private Map<String, Integer> consumes;
	private String texturePath;
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}

	public String getPredecessor() {
		return predecessor;
	}

	public void setPredecessor(String predecessor) {
		this.predecessor = predecessor;
	}

	public String getSuccessor() {
		return successor;
	}

	public void setSuccessor(String successor) {
		this.successor = successor;
	}

	public Map<String, Integer> getConsumes() {
		return consumes;
	}

	public void setConsumes(Map<String, Integer> consumes) {
		this.consumes = consumes;
	}

	public String getTexturePath() {
		return texturePath;
	}

	public void setTexturePath(String texturePath) {
		this.texturePath = texturePath;
	}
}
