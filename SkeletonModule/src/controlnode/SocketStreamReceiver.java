package controlnode;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class SocketStreamReceiver extends Thread {


	private static DatagramSocket udpServer = null;
	private SocketNode activeNode;
	private String stream = "";
	private static int listenPort = 1234;
	boolean shouldContinue = true;
	private String nodeName;
	
	public SocketStreamReceiver(SocketNode activeNode, String nodeName) throws Exception{
		udpServer = new DatagramSocket(listenPort);
		this.activeNode = activeNode;
		this.nodeName = nodeName;
	}
	
	public String getStream(){
		return stream;
	}
	
	public void stopThread(){
		System.out.println(nodeName + ": Stopping receiver thread");
		shouldContinue = false;
		udpServer.close();
	}
	
	@Override
	public void run(){
		System.out.println(nodeName + ": Receiver started");
		byte[] content = new byte[1024]; 
		while (shouldContinue){
			DatagramPacket p = new DatagramPacket(content, content.length);
			try {
				udpServer.receive(p);
				stream = new String(p.getData(), 0, p.getLength());
				System.out.println(nodeName + "'s StreamReceiver got: " + stream);
				synchronized(activeNode){
					activeNode.notify();
				}
			} catch (IOException e) {
				if(shouldContinue){ 
					/*if this flag is set, exception is out of control*/
					e.printStackTrace();
				}
				else break;
			}
		}
		System.out.println(nodeName + ": Receiver: out");
	}
}
