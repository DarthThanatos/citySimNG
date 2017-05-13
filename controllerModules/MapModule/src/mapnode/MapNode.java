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
		resources = new Resources(sender,dr);
		System.out.println("Created Map Node");
	}


	@Override
	public String parseCommand(String command, JSONObject args) {
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Map");
		if(command.equals("canAffordOnBuilding")){			
			// check if player can afford to build building
			Boolean canAffordOnBuilding = buildings.canAffordOnBuilding(args.getString("BuildingName"), resources);
			
			// create and send reply to view
			JSONObject json = new JSONObject();
			json.put("buildingID", args.getString("BuildingId"));
			json.put("buildingName", args.getString("BuildingName"));
			json.put("canAffordOnBuilding", canAffordOnBuilding);
			
			envelope.put("Operation","canAffordOnBuildingResult");
			envelope.put("Args", json);
			System.out.println("Sent after canAfford: " + envelope);
		}
		if(command.equals("placeBuilding")){
			buildings.placeBuilding(args.getString("BuildingName"), resources);
			Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
			String sign = " +";
			for(String resource : resources.getResourcesNames()){
				if(resources.getIncomes().get(resource) < 0)
				actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
						" " + resources.getIncomes().get(resource));
				else
					actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
							sign + resources.getIncomes().get(resource));
			}
			
			JSONObject json = new JSONObject();
			json.put("actualRes", actualValuseAndIncomes);
			
			envelope.put("Operation", "placeBuildingResult");
			envelope.put("Args", json);
			System.out.println("Sent after built: " + envelope);
		}
		if(command.equals("deleteBuilding")){
			buildings.deleteBuilding(args.getString("BuildingName"), resources);
			Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
			String sign = " +";
			for(String resource : resources.getResourcesNames()){
				if(resources.getIncomes().get(resource) < 0)
				actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
						" " + resources.getIncomes().get(resource));
				else
					actualValuseAndIncomes.put(resource, resources.getActualValues().get(resource) + 
							sign + resources.getIncomes().get(resource));
			}
			
			JSONObject json = new JSONObject();
			json.put("actualRes", actualValuseAndIncomes);
			
			envelope.put("Operation", "deleteBuildingResult");
			envelope.put("Args", json);
			System.out.println("Sent after delete: " + envelope);
		}
		return envelope.toString();
	}

	@Override
	public void atStart() {
		update = true;
		
		// send initial info
		resources = new Resources(sender,dr);
		buildings = new Buildings(sender,dr);
		JSONObject json = new JSONObject();
		json.put("resources", resources.getResources());
		json.put("buildings", buildings.getAllBuildings());
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Map");
		envelope.put("Operation", "Init");
		envelope.put("Args", json);
		sender.pushStreamAndWaitForResponse(envelope);
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
