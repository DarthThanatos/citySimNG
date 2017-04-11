package controlnode;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class StreamReceiver extends Thread {


	private static DatagramSocket udpServer = null;
	private static int port = 1234;
	private Node activeNode;
	private String stream = "";
	
	public StreamReceiver(Node activeNode) throws Exception{
		udpServer = new DatagramSocket();
		this.activeNode = activeNode;
	}
	
	public String getStream(){
		return stream;
	}
	
	@Override
	public void run(){
		byte[] content = new byte[1024];
		boolean shouldContinue = true;
		while (shouldContinue){
			DatagramPacket p = new DatagramPacket(content, content.length);
			try {
				udpServer.receive(p);
				stream = new String(p.getData(), 0, p.getLength());
				System.out.println(stream);
				activeNode.notify();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		udpServer.close();
	}
}
