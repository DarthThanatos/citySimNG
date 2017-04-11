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
	private static StreamReceiver activeNodeStreamReceiver = null;
	
	public Mediator(StreamReceiver activeNodeStreamReceiver){
		this.activeNodeStreamReceiver = activeNodeStreamReceiver;
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
