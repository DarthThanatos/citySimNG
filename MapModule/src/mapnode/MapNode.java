package mapnode;

import model.DependenciesRepresenter;

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
		//if(command.equals("PlaceBuilding")){
			// parse arguments
		//	String buildingName = streamArgs[0].replace(",", ",\n");
		//	System.out.println(buildingName);
			
			// check if player can afford to build building
			// Boolean canAfford = buildings.placeBuilding(buildingName, resources);
			
			// create and send reply to view
//			JSONObject json = new JSONObject();
//			synchronized(sender){
//				sender.setStream("Map@" + json);
//				sender.notify();
//				System.out.println("Sent: Map@" + json);
//			}
		//}
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
					}catch(Exception e){}
				}
			}
		};
		resourcesThread.start();
	}

	@Override
	public void atExit() {
		update = false;
	}


}
