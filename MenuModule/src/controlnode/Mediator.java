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

	private static SocketStreamReceiver activeNodeStreamReceiver = null;
	
	public Mediator(SocketStreamReceiver activeNodeStreamReceiver){
		this.activeNodeStreamReceiver = activeNodeStreamReceiver;
	}
	
	
	public static void main(String [] args){
		
	}
	
}
