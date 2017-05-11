package controlnode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class StreamSender extends Thread{
	
	private String stream = "";
	private DatagramSocket udpServer = null;
	private boolean shouldContinue = true;
	
	public StreamSender() throws Exception{
		udpServer = new DatagramSocket();
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
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void stopThread(){
		shouldContinue = false;
		this.notify();
	}
	
	public void run() {
		while(shouldContinue){
			try {
				this.wait();
				send();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		udpServer.close();
	}
}
