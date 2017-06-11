package graph;

import entities.Building;

public class BuildingNode extends GraphNode{

	private Building building;
	
	public BuildingNode(Building building) {
		this.building = building;
	}

	public String getName(){
		return building.getName();
	}
	
	public String getSuccessorName(){
		return building.getSuccessor();
	}
	
	public String getPredeccessorName(){
		return building.getPredecessor();
	}

	@Override
	public String getTexturePath() {
		return building.getTexturePath();
	}
	
}
