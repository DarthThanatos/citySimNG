package mapnode;

import model.DependenciesRepresenter;

import java.util.List;

import org.json.JSONObject;

import controlnode.SocketNode;


public class MapNode extends SocketNode{
	Thread resourcesThread;
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
			// parse arguments
			String[] argsList = streamArgs[0].split(",");
			
			// check if player can afford to build building
			Boolean canAfford = buildings.placeBuilding(argsList[0], resources);
			
			// create and send reply to view
			JSONObject json = new JSONObject();
			json.put("BuildingID", argsList[1]);
			json.put("CanAfford", canAfford);
			json.put("actualRes", resources.getActualValues());
			sender.setStream("Map@" + json);
			synchronized(sender){
				sender.notify();
			}
			
			System.out.println("Sent after built: Map@" + json);
			return "Map@" + json.toString();
		}
		return "Map@{}";
	}

	@Override
	public void atStart() {
		resources = new Resources(sender);
		buildings = new Buildings(sender);
		buildings.sendBuildingsInfo();
		resourcesThread = new Thread() {
			public void run() {
				while(update){
					resources.updateResources();
					try{
						Thread.sleep(3000);
					}catch(Exception e){
						return;
					}
				}
				System.out.println("Map timer exited while loop");
			}
		};
		resourcesThread.start();
	}

	@Override
	public void atExit() {
		this.update = false;
	}


}
