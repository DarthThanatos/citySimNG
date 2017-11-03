package graph;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import constants.Consts;

public class GraphsHolder {
	
	private List<ResourceNode> resourcesGraphs;
	private List<BuildingNode> buildingsGraphs;
	private List<DwellerNode> dwellersGraphs;
	
	private HashMap<String, ResourceNode> resourcesVertices;
	private HashMap<String, BuildingNode> buildingsVertices;
	private HashMap<String, DwellerNode> dwellersVertices;
	
	public GraphsHolder(){
		resourcesGraphs = new ArrayList<>();
		buildingsGraphs = new ArrayList<>();
		dwellersGraphs = new ArrayList<>();
	}

	public JSONObject displayAllGraphs(){
		JSONObject displayRepresentation = new JSONObject();
		JSONArray resourcesDisplayRepresentations = displayResourcesGraphs();
		displayRepresentation.put(Consts.RESOURCES, resourcesDisplayRepresentations);
		JSONArray buildingsDisplayRepresentations = displayBuildingsGraphs();
		displayRepresentation.put(Consts.BUILDINGS, buildingsDisplayRepresentations);
		JSONArray dwellersDisplayRepresentations = displayDwellersGraphs();
		displayRepresentation.put(Consts.DWELLERS, dwellersDisplayRepresentations);
		return displayRepresentation;
	}
	
	private JSONObject displayRecursively(GraphNode node){
		JSONArray children = new JSONArray();
		for (Object childObj : node.getChildren().values()){
			GraphNode child = (GraphNode) childObj;
			JSONObject childDisplayRepresentation = displayRecursively(child);
			children.put(childDisplayRepresentation);
		}
		JSONObject nodeDisplayRepresentation = new JSONObject();
		nodeDisplayRepresentation.put(Consts.TEXTURE_PATH, node.getTexturePath());
		nodeDisplayRepresentation.put(Consts.ENTITY_NAME, node.getName());
		nodeDisplayRepresentation.put(Consts.CHILDREN, children);
		nodeDisplayRepresentation.put(Consts.DETAILS, node.getConcatenatedDescription());
		return nodeDisplayRepresentation;
	}
	
	private JSONArray displayBuildingsGraphs(){
		JSONArray buildingsDisplayRepresentations = new JSONArray();
		for (BuildingNode buildingNode : buildingsGraphs){
			JSONObject rootRepresentation = displayRecursively(buildingNode);
			buildingsDisplayRepresentations.put(rootRepresentation);
		}
		return buildingsDisplayRepresentations;
	}
	
	private JSONArray displayResourcesGraphs(){
		JSONArray resourcesDisplayRepresentations = new JSONArray();
		for (ResourceNode resourceNode : resourcesGraphs){
			JSONObject rootRepresentation = displayRecursively(resourceNode);
			resourcesDisplayRepresentations.put(rootRepresentation);
		}
		return resourcesDisplayRepresentations;
	}
	
	private JSONArray displayDwellersGraphs(){
		JSONArray dwellersDisplayRepresentations = new JSONArray();
		for (DwellerNode dwellerNode : dwellersGraphs){
			JSONObject rootRepresentation = displayRecursively(dwellerNode);
			dwellersDisplayRepresentations.put(rootRepresentation);
		}
		return dwellersDisplayRepresentations;
	}
	
	
	
	public void setResourceVertices(HashMap<String, ResourceNode> resourcesVertices){
		this.resourcesVertices = resourcesVertices;		
	}
	
	public void setBuildingsVertices(HashMap<String, BuildingNode> buildingsVertices){
		this.buildingsVertices = buildingsVertices;
	}
	
	public void setDwellersVertices(HashMap<String, DwellerNode> dwellersVertices){
		this.dwellersVertices = dwellersVertices;
	}
	
	public DwellerNode getDwellerNode(String key){
		return dwellersVertices.get(key);
	}
	
	public BuildingNode getBuildingNode(String key){
		return buildingsVertices.get(key);
	}
	
	public ResourceNode getResourceNode(String key){
		return resourcesVertices.get(key);
	}
	
	public void addResourcesGraph(ResourceNode rootOfResourcesTree){
		resourcesGraphs.add(rootOfResourcesTree);
	}
	
	public void addBuildingsGraph(BuildingNode rootOfBuilingsTree){
		buildingsGraphs.add(rootOfBuilingsTree);
	}
	
	public void addDwellersGraph(DwellerNode rootOfDwellersTree){
		dwellersGraphs.add(rootOfDwellersTree);
	}
	
	public void setDwellersGraphs(List<DwellerNode> roots){
		dwellersGraphs = roots;
	}
	
	public void setBuildingsGraphs(List<BuildingNode>roots){
		buildingsGraphs = roots;
	}
	
	public void setResourcesGraphs(List<ResourceNode> roots){
		resourcesGraphs = roots;
	}
	
	public List<ResourceNode> getResourcesGraphs(){
		return resourcesGraphs;
	}
	
	public List<BuildingNode> getBuildingsGraphs(){
		return buildingsGraphs;
	}
	
	public List<DwellerNode> getDwellersGraphs(){
		return dwellersGraphs;
	}
}
