package corectness.checker;

import graph.DwellerNode;

import java.util.HashMap;

import org.json.JSONArray;

import constants.Consts;

public class DwellersChecker extends CyclesChecker{
	
	HashMap<String, DwellerNode> dwellerVertices;
	
	public DwellersChecker(JSONArray dwellers, HashMap<String, DwellerNode> dwellerVertices){
		super(dwellers, Consts.DWELLER_NAME);
		this.dwellerVertices = dwellerVertices;
	}
}
