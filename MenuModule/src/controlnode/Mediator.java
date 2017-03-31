package controlnode;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

/*
 * Class implementing communication channel between Control Layer and View Layer
 */

public class Mediator {
	
	class Sender{
		
	}
	
	class Receiver extends Thread{
		private DatagramSocket udpServer = null;
		
		public Receiver(int port){
			try {
				udpServer = new DatagramSocket(port);
			} catch (SocketException e) {
				e.printStackTrace();
			}
		}
		
		public void run(){
			while (true){
				byte[] content = new byte[1024];
				DatagramPacket p = new DatagramPacket(content, content.length);
				try {
					udpServer.receive(p);
					System.out.println(new String(p.getData(), 0, p.getLength()));
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
}
