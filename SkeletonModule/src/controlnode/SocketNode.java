package controlnode;

import java.net.DatagramSocket;
import java.util.*;

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
	
	private Node parent;
	protected String nodeName = "socket node";
	private HashMap<String, Node> neighbors;
	protected DependenciesRepresenter dr;
	
	private SocketStreamReceiver receiver = null;
	private SocketStreamSender sender = null;
		
	public SocketNode(DependenciesRepresenter dr){
		this.dr = dr;
		neighbors = new HashMap<String, Node>();
		neighbors.put("parent", parent);
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
	public abstract String parseCommand(String command, String[] streamArgs);
	
		
	public Node nodeLoop(){
		String nextNode = ""; //key of the node; it is expected to come from the view layer 
		System.out.println("\n============================================\n");
		System.out.println("Switched control to: " + nodeName);

		try {
			receiver = new SocketStreamReceiver(this, nodeName);
			sender = new SocketStreamSender(nodeName);
			receiver.start();
			sender.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		while(true){
			try {
				synchronized(this){ 
					/*needs to be in the synchronized block, otherwise it throws IllegalMonitorException*/
					this.wait();
				}
				String stream = receiver.getStream();
				String[] streamParts = stream.split("@");
				String recipentName = streamParts[0];
				String command = streamParts[1];
				String[] args = null;
				if(!recipentName.equals(nodeName)) continue; //msg not addressed to us; skipping
				if (streamParts.length > 2) 
					args = Arrays.copyOfRange(streamParts, 2, streamParts.length);
				if(command.equals("MoveTo")){
					//expecting only one argument- Node instance name to pass control to
					nextNode = args[0];
					sender.setStream("SetView@" + nextNode.replace("Node", "")); 
					// ^ we must remember that we get a node instance name adequate for a controller node, which has "Node" suffix;
					// to translate it to the form understandable to the view layer, we just have to cut off the "Node" part
					synchronized (sender){
						sender.notify();
					}
					Thread.sleep(500); 
					// ^ giving sender enough time to send its message, this may need optimizing in the future
					break;
				}
				else{ 
					String outputStream = parseCommand(command, args); //inheriting nodes will know what to do
					sender.setStream(outputStream); //setting "registers" of the sending node
					synchronized(sender){
						sender.notify(); //now we trigger our sender thread to send stream to the view layer
					}
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		//got MoveTo command, acting accordingly
		sender.stopThread();
		receiver.stopThread();
		try{
			Thread.sleep(500); 
		}catch(Exception e){
			e.printStackTrace();
		}
		return neighbors.get(nextNode);
	}
	
}
