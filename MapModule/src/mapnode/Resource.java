package mapnode;

public class Resource {
	private String name;
	private String predecessor;
	private String successor;
	private String texturePath;
	
	public Resource(String name, String predecessor, String successor, String texturePath){
		this.name = name;
		this.predecessor = predecessor;
		this.successor = successor;
		this.texturePath = texturePath;
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
}
