package graph;

import java.util.HashMap;

public class GraphNode {
	protected final String name;
	protected GraphNode parent;
	protected HashMap<String, GraphNode> children; 
	
	public GraphNode(String name){
		this.name = name;
		this.children = new HashMap<>();
	}
	
	public void setParent(GraphNode parent){
		this.parent = parent;
	}
	
	public GraphNode getParent(){
		return parent;
	}
	
	public void addChild(String name, GraphNode child){
		children.put(name, child);
	}
	
	public GraphNode getChild(String childName){
		return children.get(childName);
	}
}
