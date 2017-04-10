package controlnode;

import java.util.*;

//* This class represents an action in action graph */ 
public abstract class Node {
	
	private Node parent;
	private HashMap<String, Node> children;
	private boolean controlMine;
	
	public Node(Node parent){
		this.parent = parent;
		children = new HashMap<String, Node>();
		controlMine = false;
	}
	
	public abstract void createChildren();
	
	public void assumeControl(){
		controlMine = true;
		nodeLoop();
	}
	
	public void grantControlToChild(String childName){
		children.get(childName).assumeControl();
	}
	
	/*
	 * This method should be used to set controlMine flag to false
	 * and do any necessary cleaning 
	 */
	public void backToParent(){
		controlMine = false;
	}
	
	public void nodeLoop(){
		while(controlMine){
			
		}
	}
	
}
