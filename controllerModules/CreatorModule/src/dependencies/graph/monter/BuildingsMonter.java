package dependencies.graph.monter;

import entities.Building;
import graph.BuildingNode;
import graph.GraphsHolder;

import java.awt.dnd.DragGestureEvent;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import constants.Consts;
import corectness.checker.BuildingsChecker;
import corectness.checker.CheckException;

import org.json.JSONArray;
import org.json.JSONObject;

import model.DependenciesRepresenter;

public class BuildingsMonter extends GraphMonter{
	
	private ArrayList<Building> allBuildings;
	private JSONArray buildingsGraphDesc;
	private HashMap<String, BuildingNode> buildingVertices; 
	private DependenciesRepresenter dr;
	
	public BuildingsMonter(JSONArray buildingGraphDesc, DependenciesRepresenter dr){
		this.buildingsGraphDesc = buildingGraphDesc;
		this.dr = dr;
		allBuildings = new ArrayList<Building>();
		buildingVertices = new HashMap<>();
		List<String> buildingsNames = new ArrayList<String>();
		List<String> resourcesNames = dr.getResourcesNames();
		String relativeTexturesPath = Consts.RELATIVE_TEXTURES_PATH;
		for (int i = 0; i < buildingGraphDesc.length(); i++){
			JSONObject buildingDesc = (JSONObject)buildingGraphDesc.get(i);
			Building building = new Building();
			String buildingName = buildingDesc.getString(Consts.BUILDING_NAME);
			building.setName(buildingName);
			buildingsNames.add(buildingName);
			building.setTexturePath(relativeTexturesPath + buildingDesc.getString(Consts.TEXTURE_PATH));
			
			String predeccessor = buildingDesc.getString(Consts.PREDECESSOR);
			String successor = buildingDesc.getString(Consts.SUCCESSOR);
			building.setPredecessor(predeccessor);
			building.setSuccessor(successor);
			
			HashMap<String, Integer> consumes = new HashMap<>();
			HashMap<String, Integer> produces = new HashMap<>();
			HashMap<String, Integer> costs = new HashMap<>();
			JSONObject producedResources = buildingDesc.getJSONObject(Consts.PRODUCES);
			JSONObject consumedResources = buildingDesc.getJSONObject(Consts.CONSUMES);
			JSONObject costsDesc = buildingDesc.getJSONObject(Consts.COST_IN_RESOURCES);
			for (String resourceName : resourcesNames){
				costs.put(resourceName, 0);
				produces.put(resourceName, 0);
				consumes.put(resourceName, 0);
			}

			Iterator<?> costsDescKeys = costsDesc.keys();
			while(costsDescKeys.hasNext()){
				String requiredResource = (String)costsDescKeys.next();
				int costInResource = costsDesc.getInt(requiredResource);
				costs.put(requiredResource,costInResource);
			}
			Iterator<?> producedResourcesKeys = producedResources.keys();
			while(producedResourcesKeys.hasNext()){
				String producedResource = (String) producedResourcesKeys.next();
				int produceRate = producedResources.getInt(producedResource);
				produces.put(producedResource, produceRate);
			}
			Iterator<?> consumedResourcesKeys = consumedResources.keys();
			while(consumedResourcesKeys.hasNext()){
				String consumedResource = (String) consumedResourcesKeys.next();
				int consumeRate = consumedResources.getInt(consumedResource);
				consumes.put(consumedResource, consumeRate);
			}	
			building.setResourcesCost(costs);
			building.setConsumes(consumes);
			building.setProduces(produces);
			allBuildings.add(building);
			BuildingNode buildingNode = new BuildingNode(building);
			buildingVertices.put(buildingName, buildingNode);
		}
		dr.putModuleData(Consts.ALL_BUILDINGS, allBuildings);
		dr.setBuildingsNames(buildingsNames);
	}
	
	public ArrayList<Building> getBuildingsList(){
		return allBuildings;
	}
	
	public void mountDependenciesGraph() throws CheckException{
		BuildingsChecker buildingsChecker = new BuildingsChecker(buildingsGraphDesc, buildingVertices);
		buildingsChecker.check();
		System.out.println("buildings:");
		mountGraph(buildingVertices);
		dr.getGraphsHolder().setBuildingsGraphs(rootsList);
		dr.getGraphsHolder().setBuildingsVertices(buildingVertices);
	}
}
