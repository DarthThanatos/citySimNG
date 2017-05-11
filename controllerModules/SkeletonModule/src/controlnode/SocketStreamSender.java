package controlnode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.UUID;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.json.JSONObject;

public class SocketStreamSender extends Thread{
	
	private DatagramSocket udpServer = null;
	private boolean shouldContinue = true;
	private String nodeName;
	private BlockingQueue<String> sendQueue;
	private DispatchCenter dispatchCenter;
	
	public SocketStreamSender(String nodeName, DispatchCenter dispatchCenter) throws Exception{
		udpServer = new DatagramSocket();//udpServer;
		sendQueue = new LinkedBlockingQueue<>();
		this.nodeName = nodeName;
		this.dispatchCenter = dispatchCenter;
	}
		
	public void pushStream(String stream){
		try {
			sendQueue.put(stream);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void pushStream(JSONObject envelope){
		try {
			sendQueue.put(envelope.toString());
		} catch (InterruptedException e) {
			e.printStackTrace();
		}		
	}
	
	public void pushStreamAndWaitForResponse(JSONObject envelope){
		String operationId = UUID.randomUUID().toString();
		envelope.put("UUID", operationId);
		envelope.put("From", nodeName);
		dispatchCenter.initHandshake(nodeName, operationId);
		System.out.println("Generated " + operationId);
		try {
			sendQueue.put(envelope.toString());
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		while(!dispatchCenter.confirmed(nodeName, operationId));
		System.out.println("Blocking ended, receipt confirmed");
	}
	
	/*
	 * Algorithm of a sender based on blocking queue 
	 */
	private void queueAlgo(){
		System.out.println(nodeName + ": Sender started queue algo");
		while(true){
			try {
				String msg = sendQueue.take();
				if(shouldContinue){
					InetAddress address = InetAddress.getByName("127.0.0.1");
					DatagramPacket packet = new DatagramPacket(msg.getBytes(), msg.length(), address, 12345);
					udpServer.send(packet);
					System.out.println("[Queue algo]: " + nodeName + "'s sender: sent " + msg);
				}
				else{
					break;
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			} catch (UnknownHostException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
			
		}
		System.out.println("[Queue algo]: " + nodeName + ": Sender: out");
		udpServer.close();
	}
		
	public void stopThread(){
		System.out.println(nodeName + ": Stopping sender thread");
		shouldContinue = false;
		try {
			sendQueue.put("Quit"); 
			/*
			 * Just for sender to wake; seeing shouldContinue flag set to false, it will not try to send it anyway, but
			 * will be forced to exit its main loop
			 */ 
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("Sender stopper out");
		/*
		synchronized(this){
			this.notify();
		}*/
	}
	
	public void run() {
		queueAlgo();
	}
}
