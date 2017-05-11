package controlnode;

public interface Node{
	
	/*
	 * Main loop of each node;
	 * returns - neighbor to which control should be passed from here
	 * e.g. from a MenuNode instance we can go to CreatorNode etc. 
	 */
	public Node nodeLoop();
	
	/*
	 * This method should is used at the time when the system is created to set a reference 
	 * to the Node from which control is passed; can be modified later, as 
	 * the system lets dynamically change "dependencies" of the game logic
	 * 
	 * parentName - String, which can be used for debugging purposes,
	 * or to hash the parent if a Node instance wishes so  
	 */
	public void setParent(String parentName,Node parent);
	
	
	/*
	 * This method is used at the time when the system is created to keep track 
	 * on neighbors the flow control can be passed to from a particular Node instance;
	 * those references should then used
	 * by the nodeLoop() method to let the system know which Node is next to take control 
	 */
	public void addNeighbour(String hashKey, Node neighbour);
	
}
