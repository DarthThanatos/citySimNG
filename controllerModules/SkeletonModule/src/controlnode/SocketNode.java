package controlnode;

import java.net.DatagramSocket;
import java.util.*;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.json.JSONObject;

import model.DependenciesRepresenter;

/* 
 *  This class represents an action in the action graph 
*	First we start Threads StreamReceiver and StreamSender.
*	Then we switch control between them: Receiver is active all the time;
*	It notifies node if stream comes from view layer;
*	Node acts accordingly, sets output stream and wakes a streamSender thread. 
*	
*/ 
public abstract class SocketNode implements Node{
	
	protected Node parent;
	protected String nodeName = "socket node";
	protected HashMap<String, Node> neighbors;
	protected DependenciesRepresenter dr;
	
	protected SocketStreamReceiver receiver = null;
	protected SocketStreamSender sender = null;
	protected BlockingQueue<String> receiveQueue = null;
	protected DispatchCenter dispatchCenter;

	public Node getParent(){
		return parent;
	}

	public Node getNeighbour(String neighbourHash){
		return neighbors.get(neighbourHash);
	}
	public SocketNode(DispatchCenter dispatchCenter, String nodeName){
		this(null, dispatchCenter, nodeName);
	}
	
	public SocketNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName){
		this.dr = dr;
		this.nodeName = nodeName;
		neighbors = new HashMap<String, Node>();
		neighbors.put("parent", parent);
		receiveQueue = new LinkedBlockingQueue<String>();
		this.dispatchCenter = dispatchCenter;
	}
	
	@Override
	public void setParent(String parentName, Node parent){
		this.parent = parent;
		neighbors.put(parentName, parent);
		System.out.println(nodeName + ": put " + parentName + " as parent");
	}
	
	public void addNeighbour(String hashKey, Node neighbor){
		neighbors.put(hashKey, neighbor);
		System.out.println(nodeName + ": put " + hashKey + " as neighbour");
	}
	
	/*
	 * command - text of command, extending node should know what to do with it and act accordingly
	 * streamArgs - arguments necessary for this command
	 * returns: String that needs to be send to the view layer
	 */
	public abstract String parseCommand(String command, JSONObject args);
	
	public abstract void atStart();
	public abstract void atExit();
		
	public Node nodeLoop(){
		String nextNode = ""; //key of the node; it is expected to come from the view layer 
		System.out.println("\n============================================\n");
		System.out.println("Switched control to: " + nodeName);
		
		try {
			receiver = new SocketStreamReceiver(nodeName, receiveQueue);
			sender = new SocketStreamSender(nodeName, dispatchCenter);
			receiver.start();
			sender.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
		JSONObject envelope = new JSONObject();
		envelope.put("To", "ViewSetter");
		envelope.put("Operation", "SetView");
		JSONObject setViewArgs = new JSONObject();
		setViewArgs.put("TargetView", nodeName.replace("Node",""));
		// ^ we must remember that we get a node instance name adequate for a controller node, which has "Node" suffix;
		// to translate it to the form understandable to the view layer, we just have to cut off the "Node" part
		envelope.put("Args", setViewArgs);
		sender.pushStreamAndWaitForResponse(envelope);
		atStart();
		
		while(true){
			try {
				String stream = receiveQueue.take();
				JSONObject jsonMsg = new JSONObject(stream);
				String recipentName = jsonMsg.getString("To");
				String command = jsonMsg.getString("Operation");
				JSONObject args = jsonMsg.getJSONObject("Args");
				System.out.println("Recipent: " + recipentName + " cmd: " + command + " args: " + args);
				if(!recipentName.equals(nodeName)) continue; //msg not addressed to us; skipping
				if(command.equals("MoveTo")){
					//expecting only one argument- Node instance name to pass control to
					nextNode = args.getString("TargetControlNode");
					break;
				}
				else{ 
					String outputStream = parseCommand(command, args); //inheriting nodes will know what to do
					sender.pushStream(outputStream);
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		//got MoveTo command, acting accordingly
		
		sender.stopThread();
		receiver.stopThread();
		try {
			sender.join();
			receiver.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		atExit();
		return neighbors.get(nextNode);
	}
	
	public String getNodeName(){
		return nodeName;
	}
	
}
