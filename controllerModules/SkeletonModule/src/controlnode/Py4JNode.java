package controlnode;

import java.util.HashMap;
import java.util.concurrent.LinkedBlockingQueue;

import py4jmediator.Presenter;
import model.DependenciesRepresenter;

public abstract class Py4JNode implements Node{

	protected Node parent;
	protected String nodeName = "socket node";
	protected HashMap<String, Node> neighbors;
	protected DependenciesRepresenter dr;
	protected DispatchCenter dispatchCenter;
	
	private Node nextNode;
	private volatile boolean shouldLooping = true;

	public Py4JNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName){
		this.dr = dr;
		this.nodeName = nodeName;
		neighbors = new HashMap<String, Node>();
		this.dispatchCenter = dispatchCenter;
	}
	
	@Override
	public void setParent(String parentName, Node parent){
		this.parent = parent;
		neighbors.put(parentName, parent);
		System.out.println(nodeName + "py4j: put " + parentName + " as parent");
	}
	
	public void addNeighbour(String hashKey, Node neighbor){
		neighbors.put(hashKey, neighbor);
		System.out.println(nodeName + " py4j: put " + hashKey + " as neighbour");
	}
	
	protected void moveTo(String targetName){
		nextNode = neighbors.get(targetName);
		shouldLooping = false;
	}

	
	protected abstract void atStart();
	protected abstract void onLoop();
	protected abstract void atExit(); 	
	
	@Override
	public String getNodeName() {
		return nodeName;
	}
	
	@Override
	public Node nodeLoop() {
		shouldLooping = true;
		atStart();
		while(shouldLooping){
			onLoop();
		}
		atExit();
		return nextNode;
	}

}
