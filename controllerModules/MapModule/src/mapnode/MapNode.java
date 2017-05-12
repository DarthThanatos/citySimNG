package mapnode;

import model.DependenciesRepresenter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONObject;

import controlnode.DispatchCenter;
import controlnode.SocketNode;


public class MapNode extends SocketNode{
	Thread resourcesThread;
	public boolean update = true;
	public Buildings buildings;
	Resources resources = null;
	
	public MapNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		resources = new Resources(sender);
		System.out.println("Created Map Node");
	}


	@Override
	public String parseCommand(String command, JSONObject args) {
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Map");
		if(command.equals("canAffordOnBuilding")){
			// parse arguments
			//String[] argsList = streamArgs[0].split(",");
			
			// check if player can afford to build building
			Boolean canAffordOnBuilding = buildings.canAffordOnBuilding(args.getString("BuildingName"), resources);
			
			// create and send reply to view
			JSONObject json = new JSONObject();
			json.put("buildingID", args.getString("BuildingId"));
			json.put("buildingName", args.getString("BuildingName"));
			json.put("canAffordOnBuilding", canAffordOnBuilding);
			
			envelope.put("Operation","canAffordOnBuildingResult");
			envelope.put("Args", json);
			/*sender.setStream("Map@" + json);
			synchronized(sender){
				sender.notify();
			}*/
			System.out.println("Sent after canAfford: " + envelope);
			//return "Map@" + json.toString();
		}
		if(command.equals("placeBuilding")){
			buildings.placeBuilding(args.getString("BuildingName"), resources);
			Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
			String sign = " +";
			for(String resource : resources.getResourcesNames()){
				if(resources.getIncomes().get(resource) < 0)
					sign = " ";
				actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
						sign + resources.getIncomes().get(resource));
			}
			
			JSONObject json = new JSONObject();
			json.put("actualRes", actualValuseAndIncomes);
			
			envelope.put("Operation", "placeBuildingResult");
			envelope.put("Args", json);
			System.out.println("Sent after built: " + envelope);
		}
		return envelope.toString();
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
		/*sender.setStream("Map@" + json);
		synchronized(sender){
			sender.notify();
		} */
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Map");
		envelope.put("Operation", "Init");
		envelope.put("Args", json);
		sender.pushStreamAndWaitForResponse(envelope);
		//sender.pushStream("Map@" + json);
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


	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}


}
