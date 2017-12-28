package controlnode;

import java.util.HashMap;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import model.DependenciesRepresenter;

public abstract class Py4JNode implements Node{

	protected Node parent;
	protected String nodeName = "socket node";
	protected HashMap<String, Node> neighbors;
	protected DependenciesRepresenter dr;
	protected DispatchCenter dispatchCenter;
	
	private Node nextNode;
//	private volatile boolean looping = true;

	public Node getParent(){
		return parent;
	}

	public Node getNeighbour(String neighbourHash){
		return neighbors.get(neighbourHash);
	}

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
	}
	
	public void addNeighbour(String hashKey, Node neighbor){
		neighbors.put(hashKey, neighbor);
	}
	
	protected void moveTo(String targetName){
		nextNode = neighbors.get(targetName);
//		looping = false;
		lock.lock();
		looping.signal();
		lock.unlock();
	}

	
	protected abstract void atStart();
	protected abstract void atExit(); 	
	
	@Override
	public String getNodeName() {
		return nodeName;
	}

	private final Lock lock = new ReentrantLock();
	private Condition looping = lock.newCondition();

	@Override
	public Node nodeLoop() {
//		looping = true;
		atStart();
//		while(looping){
//			onLoop();
//		}

		lock.lock();
		try{
			looping.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			lock.unlock();
		}
		atExit();
		return nextNode;
	}

	@Override
	public void atUnload() {
		for (Node neighbor : neighbors.values()){
			if (neighbor != parent){
				neighbor.atUnload();
			}
		}
	}
}
