package controlnode;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.concurrent.BlockingQueue;

public class SocketStreamReceiver extends Thread {


	private static DatagramSocket udpServer = null;
	private String stream = "";
	private static int listenPort = 1234;
	boolean shouldContinue = true;
	private String nodeName;
	private BlockingQueue<String> receiveQueue;
	
	public SocketStreamReceiver(String nodeName, BlockingQueue<String> receiveQueue) throws Exception{
		udpServer = new DatagramSocket(listenPort);
		this.nodeName = nodeName;
		this.receiveQueue = receiveQueue;
	}
	
	public String getStream(){
		return stream;
	}
	
	public void stopThread(){
		System.out.println(nodeName + ": Stopping receiver thread");
		shouldContinue = false;
		udpServer.close();
		System.out.println("Receiver stopper out");
	}
	
	@Override
	public void run(){
		System.out.println(nodeName + ": Receiver started");
		byte[] content = new byte[100000]; 
		while (shouldContinue){
			DatagramPacket p = new DatagramPacket(content, content.length);
			try {
				udpServer.receive(p);
				stream = new String(p.getData(), 0, p.getLength());
				System.out.println(nodeName + "'s StreamReceiver got: " + stream);
				/*synchronized(activeNode){
					activeNode.notify();
				}*/
				receiveQueue.put(stream);
			} catch (IOException e) {
				if(shouldContinue){ 
					/*if this flag is set, exception is out of control*/
					e.printStackTrace();
				}
				else break;
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		System.out.println(nodeName + ": Receiver: out");
	}
}
