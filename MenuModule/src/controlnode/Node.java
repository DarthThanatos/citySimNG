package controlnode;

import java.util.*;

//* This class represents an action in action graph */ 
public abstract class Node {
	
	private Node parent;
	private HashMap<String, Node> neighbours;
	private boolean controlMine;
	
	private StreamReceiver receiver = null;
	private StreamSender sender = null;
	
	public Node(Node parent){
		this.parent = parent;
		neighbours = new HashMap<String, Node>();
		neighbours.put("parent", parent);
		try {
			receiver = new StreamReceiver(this);
			sender = new StreamSender();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * This method should be used by descendants extending this class 
	 * to properly mount graph of dependencies between possible communication flows 
	 */
	public abstract void createChildren();
	
	/*
	 * command - text of command, extending node should know what to do with it and act accordingly
	 * streamArgs - arguments necessary for this command
	 */

	public abstract void parseCommand(String command, String[] streamArgs);
	
		
	public void nodeLoop(){
		String nextNode = "";
		while(true){
			try {
				this.wait();
				String stream = receiver.getStream();
				String[] streamParts = stream.split("@");
				String command = streamParts[0];
				String[] args = Arrays.copyOfRange(streamParts, 1, streamParts.length - 1);
				if(command.equals("MoveTo")){
					//expecting only one argument
					nextNode = args[1];
					break;
				}
				else{ 
					parseCommand(command, args);
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		//got MoveTo command, acting accordingly
		sender.stopThread();
		receiver.
	}
	
}
