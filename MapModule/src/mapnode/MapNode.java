package mapnode;

import model.DependenciesRepresenter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
			Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
			String sign = " +";
			for(String resource : resources.getResourcesNames()){
				if(resources.getIncomes().get(resource) < 0)
					sign = " ";
				actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
						sign + resources.getIncomes().get(resource));
			}
			JSONObject json = new JSONObject();
			json.put("buildingID", argsList[1]);
			json.put("canAfford", canAfford);
			json.put("actualRes", actualValuseAndIncomes);
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
		update = true;
		
		// send initial info
		resources = new Resources(sender);
		buildings = new Buildings(sender);
		JSONObject json = new JSONObject();
		json.put("resources", resources.getResources());
		json.put("buildings", buildings.getAllBuildings());
		sender.setStream("Map@" + json);
		synchronized(sender){
			sender.notify();
		} 
		
		resourcesThread = new Thread() {
			public void run() {
				while(update){
					resources.updateResources();
					try{
						Thread.sleep(3000);
					}catch(Exception e){
						System.out.println("Map timer exited while loop");
					}
				}
				System.out.println("Map timer exited while loop");
			}
		};
		resourcesThread.start();
	}

	@Override
	public void atExit() {
		resourcesThread.interrupt();
		this.update = false;
	}


}
