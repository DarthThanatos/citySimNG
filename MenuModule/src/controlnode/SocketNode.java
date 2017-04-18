package controlnode;

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
	private HashMap<String, Node> neighbours;
	protected DependenciesRepresenter dr;
	
	private SocketStreamReceiver receiver = null;
	private SocketStreamSender sender = null;
		
	public SocketNode(Node parent, DependenciesRepresenter dr){
		this.parent = parent;
		this.dr = dr;
		neighbours = new HashMap<String, Node>();
		neighbours.put("parent", parent);
		try {
			receiver = new SocketStreamReceiver(this);
			sender = new SocketStreamSender();
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
	 * returns: String that needs to be send to the view layer
	 */

	public abstract String parseCommand(String command, String[] streamArgs);
	
		
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
					String outputStream = parseCommand(command, args); //inheriting nodes will know what to do
					sender.setStream(outputStream); //setting "registers" of the sending node
					sender.notify(); //now we trigger our sender thread to send stream to the view layer
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		//got MoveTo command, acting accordingly
		sender.stopThread();
		receiver.stop();
		neighbours.get(nextNode).nodeLoop();
	}
	
}
