//package mapnode;
//
//import model.DependenciesRepresenter;
//
//import java.util.HashMap;
//import java.util.List;
//import java.util.Map;
//
//import org.json.JSONObject;
//
//import controlnode.DispatchCenter;
//import controlnode.SocketNode;
//
//
//public class MapNode extends SocketNode{
//	Thread resourcesThread;
//	public boolean update = true;
//	public Buildings buildings;
//	public Dwellers dwellers;
//	Resources resources = null;
//	boolean initialized = false;
//
//	public MapNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
//		super(dr, dispatchCenter, nodeName);
//		resources = new Resources(sender,dr);
//		dwellers = new Dwellers(sender, dr);
//		System.out.println("Created Map Node");
//	}
//
//
//	@Override
//	public String parseCommand(String command, JSONObject args) {
//		JSONObject envelope = new JSONObject();
//		envelope.put("To", "Map");
//
//		if(command.equals("canAffordOnBuilding")){
//			// check if player can afford to build building
//			Boolean canAffordOnBuilding = buildings.canAffordOnBuilding(args.getString("BuildingName"), resources);
//
//			// create and send reply to view
//			JSONObject json = new JSONObject();
//			json.put("buildingID", args.getString("BuildingId"));
//			json.put("buildingName", args.getString("BuildingName"));
//			json.put("canAffordOnBuilding", canAffordOnBuilding);
//
//			envelope.put("Operation","canAffordOnBuildingResult");
//			envelope.put("Args", json);
//			System.out.println("Sent after canAfford: " + envelope);
//		}
//
//		if(command.equals("placeBuilding")){
//			buildings.placeBuilding(args.getString("BuildingName"), args.getString("BuildingId"),
//					resources, dwellers);
//			// Map<String, String> resourceInfoMap = createResourcesInfoMap();
//
//			JSONObject json = new JSONObject();
//			json.put("actualValues", resources.getActualResourcesValues());
//			json.put("actualIncomes", resources.getResourcesBalance());
//			json.put("currDwellersAmount", dwellers.getNeededDwellers());
//			json.put("currDwellersMaxAmount", dwellers.getAvailableDwellers());
//
//			envelope.put("Operation", "placeBuildingResult");
//			envelope.put("Args", json);
//			System.out.println("Sent after built: " + envelope);
//		}
//
//		if(command.equals("deleteBuilding")){
//			buildings.deleteBuilding(args.getString("BuildingId"), resources, dwellers);
//			//Map<String, String> actualValuseAndIncomes = createResourcesInfoMap();
//
//			JSONObject json = new JSONObject();
//			json.put("actualValues", resources.getActualResourcesValues());
//			json.put("actualIncomes", resources.getResourcesBalance());
//			json.put("currDwellersAmount", dwellers.getNeededDwellers());
//
//			envelope.put("Operation", "deleteBuildingResult");
//			envelope.put("Args", json);
//			System.out.println("Sent after delete: " + envelope);
//		}
//
//		if(command.equals("stopProduction")){
//			buildings.stopProduction(args.getString("BuildingId"), resources, dwellers);
//			//Map<String, String> actualValuseAndIncomes = createResourcesInfoMap();
//
//			JSONObject json = new JSONObject();
//			json.put("actualValues", resources.getActualResourcesValues());
//			json.put("actualIncomes", resources.getResourcesBalance());
//			json.put("currDwellersAmount", dwellers.getNeededDwellers());
//			json.put("currDwellersMaxAmount", dwellers.getAvailableDwellers());
//
//			// TODO: mby we should keep this info in view
//			json.put("buildingState", buildings.findBuildingWithId(args.getString("BuildingId")).isRunning());
//
//			envelope.put("Operation", "stopProductionResult");
//			envelope.put("Args", json);
//			System.out.println("Sent after delete: " + envelope);
//		}
//
////		if(command.equals("getBuildingState")){
////			envelope.put("Operation", "getBuildingStateResult");
////			envelope.put("Args", buildings.getBuildingState(args.getString("BuildingId")));
////		}
//
//		return envelope.toString();
//	}
//
//	@Override
//	public void atStart() {
//		update = true;
//		if(!initialized){
//
//			// send initial info
//			resources = new Resources(sender,dr);
//			buildings = new Buildings(sender,dr);
//			JSONObject json = new JSONObject();
//			json.put("resources", resources.getResources());
//			json.put("buildings", buildings.getAllBuildings());
//			json.put("dewellers", dwellers.getAllDewellers());
//			json.put("initialResourcesValues", resources.getActualResourcesValues());
//			json.put("initialResourcesIncomes", resources.getResourcesBalance());
//			json.put("Texture One", dr.getTextureAt(0));
//			json.put("Texture Two", dr.getTextureAt(1));
//			JSONObject envelope = new JSONObject();
//			envelope.put("To", "Map");
//			envelope.put("Operation", "Init");
//			envelope.put("Args", json);
//			sender.pushStreamAndWaitForResponse(envelope);
//			resourcesThread = new Thread() {
//				public void run() {
//					while(update){
//						resources.calculateCurrentCycle();
//						try{
//							Thread.sleep(3000);
//						}catch(Exception e){
//							System.out.println("Map timer exited while loop");
//						}
//					}
//					System.out.println("Map timer exited while loop");
//				}
//			};
//			resourcesThread.start();
//			initialized = true;
//		}
//		else{
//			resources.setSender(sender);
//			resourcesThread = new Thread() {
//				public void run() {
//					while(update){
//						resources.calculateCurrentCycle();
//						try{
//							Thread.sleep(3000);
//						}catch(Exception e){
//							System.out.println("Map timer exited while loop");
//						}
//					}
//					System.out.println("Map timer exited while loop");
//				}
//			};
//			resourcesThread.start();
//		}
//	}
//
//	@Override
//	public void atExit() {
//		resourcesThread.interrupt();
//		this.update = false;
//	}
//
//
//	@Override
//	public void atUnload() {
//
//	}
//
//	private Map<String, String> createResourcesInfoMap(){
//		Map<String, String> resourceInfoMap = new HashMap<String, String>();
//
//		for(String resource : resources.getResourcesNames()){
//			if(resources.getResourcesBalance().get(resource) < 0)
//				resourceInfoMap.put(resource, resources.getActualResourcesValues().get(resource) +
//					" " + resources.getResourcesBalance().get(resource));
//			else
//				resourceInfoMap.put(resource, resources.getActualResourcesValues().get(resource) +
//						" + " + resources.getResourcesBalance().get(resource));
//		}
//		return resourceInfoMap;
//	}
//}
