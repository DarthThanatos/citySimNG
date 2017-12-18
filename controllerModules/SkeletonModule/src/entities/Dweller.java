package entities;

import utils.CollectionConcatenationUtils;

import java.util.Map;

public class Dweller extends Entity{
	private Map<String, Integer> consumes;

	
	public Dweller(){
		
	}

	public Map<String, Integer> getConsumes() {
		return consumes;
	}

	public void setConsumes(Map<String, Integer> consumes) {
		this.consumes = consumes;
	}

	@Override public String toString(){
		return "Dweller name: " + getName()
				+ "\n=====================\n"
				+ "Description:\n" + description
				+ "\n=====================\n"
				+ "Consumes:\n" + CollectionConcatenationUtils.filteredMapToString(consumes);

	}
}
