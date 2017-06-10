package graph;

import java.util.HashSet;
import java.util.Set;

public class ResourceNode extends GraphNode{

	private Set<String> assignedDomesticBuildings;
	
	public ResourceNode(String name) {
		super(name);
		assignedDomesticBuildings = new HashSet<String>();
	}
	
	public void setAssignedBuilding(String assignedBuildingName){
		//assignedBuilding = assignedBuildingName;
	}
	
	

}
