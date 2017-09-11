package corectness.checker;

import entities.Building;
import graph.BuildingNode;

import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import constants.Consts;

public class BuildingsChecker extends CyclesChecker {
	HashMap<String, BuildingNode> buildingsVertices;
	
	public BuildingsChecker(JSONArray buildings, HashMap<String, BuildingNode> buildingsVertices){
		super(buildings, Consts.BUILDING_NAME);
		this.buildingsVertices = buildingsVertices;
	}

	
}
