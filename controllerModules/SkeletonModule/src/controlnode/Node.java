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
	
	/*
	 * When this method is called, the caller wants to replace
	 * an existing instance of node by the new one (in particular
	 * LoaderNode will call it at the time new set of rule has to
	 * be applied); this is a signal given to the node to cleanup
	 * and release system resources, stop any running threads etc.
	 * Note that this is different than the end of a nodeLoop cycle of a node;
	 * after this call, this node will be no more referenced to, as it has been
	 * replaced by a new node with new configuration.
	 */
	public void atUnload();
	
	
	/*
	 * Operation needed for runtime change in control flow graph; 
	 * e.g. LoaderNode instance will need hashKey of next menu and previous menu 
	 * 
	 */
	public String getNodeName();

	public Node getNeighbour(String neighbourHash);
	public Node getParent();
}
