package entities;

import constants.Consts;
import constants.CreatorConfig;

public class Resource extends Entity {
	private int startingIncome;
	

	public Resource(){
		setName("Resource");
		setStartingIncome(0);
		setPredecessor("None");
		setSuccessor("None");
		setTexturePath(CreatorConfig.TEXTURE_ONE_DEFAULT_NAME);
		setDescription("Description");
	}
	
	public Resource(String name, String predecessor, String successor, String texturePath, String description, int startIncome){
		setName(name);
		setStartingIncome(startIncome);
		setPredecessor(predecessor);
		setSuccessor(successor);
		setTexturePath(texturePath);
		setDescription(description);
	}
	
	public void setStartingIncome(int startingIncome){
		this.startingIncome = startingIncome;
	}
	
	public int getStartingIncome(){
		return startingIncome;
	}

	@Override public String toString(){
		return "Resource name: " + getName()
				+ "\n=====================\n"
				+ "Description:\n" + description
				+ "\n=====================\n"
				+ "Starting income: " + startingIncome;

	}
}
