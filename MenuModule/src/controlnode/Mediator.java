package controlnode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

/*
 * Class implementing communication channel between Control Layer and View Layer
 */

public class Mediator {

	private static DatagramSocket udpServer = null;
	private static int port = 1234;
	
	static class Receiver extends Thread{
				
		public void run(){
			while (true){
				byte[] content = new byte[1024];
				DatagramPacket p = new DatagramPacket(content, content.length);
				try {
					udpServer.receive(p);
					System.out.println(new String(p.getData(), 0, p.getLength()));
					udpServer.close();
					break;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
	
	
	class Sender extends Thread{
		String jsonPath;
		
		public Sender(String jsonPath){
			this.jsonPath = jsonPath;
		}
		
		public void run(){
			try {
				BufferedReader br = new BufferedReader(new FileReader(new File(jsonPath)));
				String line, res = "";
				while ((line = br.readLine())!= null){
					res += line;
				}
				res += "\n";
				InetAddress address = InetAddress.getByName("127.0.0.1");
				DatagramPacket packet = new DatagramPacket(res.getBytes(), res.length(), address, 12345);
				udpServer.send(packet);
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void send(String jsonPath){
		Sender sender = new Sender(jsonPath);
		sender.start();
	}
	
	public static void main(String [] args){
		try {
			udpServer = new DatagramSocket(port);
			new Receiver().start();
			new Mediator().send("file.json");
		} catch (SocketException e) {
			e.printStackTrace();
		}
	}
	
}
