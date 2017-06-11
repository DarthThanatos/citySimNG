package graph;

import java.util.HashMap;

public abstract class GraphNode {
	protected GraphNode parent;
	protected HashMap<String, GraphNode> children; 
	protected GraphNode successor;
	protected GraphNode predeccessor;
	
	public GraphNode(){
		this.children = new HashMap<>();
	}
	
	public void setParent(GraphNode parent){
		this.parent = parent;
	}
	
	public void setSuccessor(GraphNode successor){
		this.successor = successor;
	}
	
	public void setPredeccessor(GraphNode predeccessor){
		this.predeccessor = predeccessor;
	}
	
	public GraphNode getSucceessor(){
		return successor;
	}
	
	public GraphNode getPredecessor(){
		return predeccessor;
	}
	
	public GraphNode getParent(){
		return parent;
	}
	
	public abstract String getTexturePath();
	public abstract String getName();
	
	public void addChild(String name, GraphNode child){
		children.put(name, child);
	}
	
	public GraphNode getChild(String childName){
		return children.get(childName);
	}
	
	public HashMap getChildren(){
		return children;
	}
	
	public abstract String getSuccessorName();
	public abstract String getPredeccessorName();
}
