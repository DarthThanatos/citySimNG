package entities;

public class Resource {
	private String name;
	private String predecessor;
	private String successor;
	private String texturePath;
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
		this.name = name;
		this.predecessor = predecessor;
		this.successor = successor;
		this.texturePath = texturePath;
	}
	
	public void setStartingIncome(int startingIncome){
		this.startingIncome = startingIncome;
	}
	
	public int getStartingIncome(){
		return startingIncome;
	}
	
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

	public String getTexturePath() {
		return texturePath;
	}

	public void setTexturePath(String texturePath) {
		this.texturePath = texturePath;
	}

	@Override public String toString(){
		return "Resource name: " + name
				+ "\n=====================\n"
				+ "Description:\n" + description
				+ "\n=====================\n"
				+ "Starting income: " + startingIncome;

	}
}
