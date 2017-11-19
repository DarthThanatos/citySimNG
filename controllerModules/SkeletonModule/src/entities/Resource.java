package entities;

public class Resource extends Entity {
	private int startingIncome;
	private String description;
	
	public String getDescription(){
		return description;
	}
	
	public void setDescription(String description){
		this.description = description;
	}
	
	public Resource(){
		
	}
	
	public Resource(String name, String predecessor, String successor, String texturePath){
		setName(name);
		setPredecessor(predecessor);
		setSuccessor(successor);
		setTexturePath(texturePath);
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
