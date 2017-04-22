package mapnode;

import model.DependenciesRepresenter;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.json.JSONObject;

import controlnode.Node;
import controlnode.SocketNode;
import controlnode.SocketStreamReceiver;
import controlnode.SocketStreamSender;

public class MapNode extends SocketNode{
	Runnable resourcesThread;
	public boolean update = true;
	public Buildings buildings;
	Resources resources = new Resources(sender);
	
	public MapNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("Created Map Node");
		nodeName = "MapNode";
	}


	@Override
	public String parseCommand(String command, String[] streamArgs) {
		if(command.equals("PlaceBuilding")){
			String arg = streamArgs[0].replace(",", ",\n");
			Boolean c =buildings.placeBuilding(arg, resources);
			JSONObject json = new JSONObject("{can:" + c.toString() + "}");
			synchronized(sender){
			sender.setStream("Map@" + json);
			sender.notify();
			System.out.println("Sent: Map@" + json);
			}
		}
		return "Map@Msg received successfully";
	}

	@Override
	public void atStart() {
		resources = new Resources(sender);
		buildings = new Buildings(sender);
		buildings.sendBuildingsInfo();
		resourcesThread = new Runnable() {
			public void run() {
				while(update){
					resources.updateResources();
					try{
						Thread.sleep(3000);
					}catch(Exception e){}
				}
			}
		};
		resourcesThread.run();
	}

	@Override
	public void atExit() {
		update = false;
	}


}
