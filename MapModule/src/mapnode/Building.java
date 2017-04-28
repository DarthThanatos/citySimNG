package mapnode;

import java.util.List;
import java.util.Map;

public class Building {
	private String name;
	private String dewellerName;
	private String texture;
	private Map<String, Integer> resourcesCost;
	private Map<String, Integer> produces;
	private Map<String, Integer> consumes;
	
	public String getTexture() {
		return texture;
	}
	
	public void setTexture(String texture) {
		this.texture = texture;
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

	public String getDewellerName() {
		return dewellerName;
	}

	public void setDewellerName(String dewellerName) {
		this.dewellerName = dewellerName;
	}
	
}
