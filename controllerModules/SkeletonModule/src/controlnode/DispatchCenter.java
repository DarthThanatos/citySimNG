package controlnode;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;
import java.util.UUID;

import com.google.common.eventbus.EventBus;
import org.json.JSONObject;

/*
 * This class' task is to wait for any incoming data either via normal method call or by
 * a thread delegated to listen on a specific port.
 * Then, when a query for specific data comes, it serves the caller by searching through its 
 * local store, returning an Object or null if nothing was found. 
 * The instance of this class should be used for acknowledgments coming from view layer  
 * (for now, when a data is sent to the view, there is no way of telling if it already came, and 
 * some actions need synchronization between logic and view, like switching between nodes, or sending
 * some long initializing json data before any other messages)
 * or communication between modules' threads (for example, as the means of notification for 
 * MapModule, that TutorialModule has some processed text for the former to be taken 
 * and perhaps displayed by its view equivalent).
 * However, please, do note that this should not be used for communication between 
 * SocketNode instances and their direct views; for this purpose SocketStream* classes were implemented.
 * 
 * A proposed convention for acknowledgments in this class is to use generated beforehand UUID strings;
 * keys for storing data for the sake of communication between modules' threads can be arbitrary.
 * 
 * @param acknowledgemntsSocket - thread waiting for acknowledgments coming from view layer will be 
 * listening on that socket
 * 
 * @param dispathData - hashmap database for storing any kind of objects (for acknowledgments 
 * those will be Boolean instances - true: received, false: not yet).    
 */

public class DispatchCenter{
	HashMap<String,HashMap<String, Object>> dispatchData;
	private EventBus eventBus;

	public DispatchCenter(){
		dispatchData = new HashMap<>();
		eventBus = new EventBus();
		new AcknowledgementWaiter().start();
	}

	public EventBus getEventBus() {
		return eventBus;
	}

	class AcknowledgementWaiter extends Thread{
		DatagramSocket acknowledgmentsSocket;
		AcknowledgementWaiter(){
			try {
				acknowledgmentsSocket = new DatagramSocket(2468);
			} catch (SocketException e) {
				e.printStackTrace();
			}
		}
		
		@Override
		public void run(){
			while(true){
				byte[] buffer = new byte[1024];
				DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
				try {
					acknowledgmentsSocket.receive(packet);
					String jsonAcknowledgmentDesc = new String(packet.getData(), 0, packet.getLength());
					JSONObject jsonObj = new JSONObject(jsonAcknowledgmentDesc);
					String receivingModule = jsonObj.getString("To");
					String operationUUID = jsonObj.getString("UUID");
					dispatchData.get(receivingModule).put(operationUUID, true);
					System.out.println("Receiving module: " + receivingModule + " has acknowledged operation with UUID: " + operationUUID);
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}

	
	public void createDB(List<String> modulesNamesList){
		for (String moduleName : modulesNamesList){
			dispatchData.put(moduleName, new HashMap<>());
		}
	}
	
	void initHandshake(String moduleName, String uuid){
		dispatchData.get(moduleName).put(uuid, false);
	}
	
	boolean confirmed(String moduleName, String uuid){
		return (Boolean) dispatchData.get(moduleName).get(uuid); 
	}
	
	public void putDispatchData(String module, String key, Object dispatch){
		if (!dispatchData.containsKey(module)) dispatchData.put(module, new HashMap<String, Object>());
		dispatchData.get(module).put(key,dispatch);
	}

	public Object getDispatchData(String module, String key){
		return dispatchData.get(module).get(key);
	}
}
