package entities;

import constants.CreatorConfig;
import utils.CollectionConcatenationUtils;

import java.util.HashMap;
import java.util.Map;

public class Dweller extends Entity{
	private Map<String, Integer> consumes;

	
	public Dweller(){
		setName("Dweller");
		setConsumes(new HashMap<String, Integer>(){{put("Resource",1);}});
		setDescription("Description");
		setPredecessor("None");
		setSuccessor("None");
		setTexturePath(CreatorConfig.TEXTURE_ONE_DEFAULT_NAME);
	}

	public Dweller(String name, String predecessor, String successor, String texturePath, String description){
		setName(name);
		setPredecessor(predecessor);
		setSuccessor(successor);
		setTexturePath(texturePath);
		this.description = description;
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
