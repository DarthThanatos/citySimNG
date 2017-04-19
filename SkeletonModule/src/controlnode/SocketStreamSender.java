package controlnode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class SocketStreamSender extends Thread{
	
	private String stream = "";
	private DatagramSocket udpServer = null;
	private boolean shouldContinue = true;
	private String nodeName;
	
	public SocketStreamSender(String nodeName) throws Exception{
		udpServer = new DatagramSocket();//udpServer;
		this.nodeName = nodeName;
	}
	
	public void setStream(String stream){
		this.stream = stream;
	}
	
	public void mountAndSentJson(String jsonPath) throws Exception{
		BufferedReader br = new BufferedReader(new FileReader(new File(jsonPath)));
		String line, res = "";
		while ((line = br.readLine())!= null){
			res += line;
		}
		res += "\n";	
		stream = res;
		br.close();
	}
	
	private void send(){
		try {
			InetAddress address = InetAddress.getByName("127.0.0.1");
			DatagramPacket packet = new DatagramPacket(stream.getBytes(), stream.length(), address, 12345);
			udpServer.send(packet);
			System.out.println(nodeName + ": sent " + stream);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void stopThread(){
		System.out.println(nodeName + ": Stopping sender thread");
		shouldContinue = false;
		synchronized(this){
			this.notify();
		}
	}
	
	public void run() {
		System.out.println(nodeName + ": Sender started");
		while(true){
			try {
				synchronized(this){
					this.wait();
				}
				if(shouldContinue) send();
				else break;
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		System.out.println(nodeName + ": Sender: out");
		udpServer.close();
	}
}
