package corectness.checker;

import graph.BuildingNode;

import java.util.HashMap;

import org.json.JSONArray;

import constants.Consts;

public class BuildingsChecker extends CyclesChecker {
	HashMap<String, BuildingNode> buildingsVertices;
	
	public BuildingsChecker(JSONArray buildings, HashMap<String, BuildingNode> buildingsVertices){
		super(buildings, Consts.BUILDING_NAME);
		this.buildingsVertices = buildingsVertices;
	}
}
