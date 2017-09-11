package dependencies.graph.monter;

import entities.Building;
import entities.Dweller;
import entities.Resource;
import graph.BuildingNode;
import graph.DwellerNode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import model.DependenciesRepresenter;

import org.json.JSONArray;
import org.json.JSONObject;

import constants.Consts;
import corectness.checker.CheckException;
import corectness.checker.DwellersChecker;

public class DwellersMonter extends GraphMonter{

	private JSONArray dwellersGraphDesc;
	private HashMap<String, DwellerNode> dwellerVertices;
	private DependenciesRepresenter dr;
	
	public DwellersMonter(List<Dweller> dwellers, DependenciesRepresenter dr){
		this.dwellersGraphDesc = listToJSONArray(dwellers);
		this.dr = dr;
		dwellerVertices = new HashMap<>();
		List<String> dwellersNames = new ArrayList<String>();
		for (Dweller dweller : dwellers){
			String dwellerName = dweller.getName();
			DwellerNode dwellerNode = new DwellerNode(dweller);
			dwellerVertices.put(dwellerName, dwellerNode);
			dwellersNames.add(dwellerName);
		}
		
	}

	public DwellersMonter(JSONArray dwellersGraphDesc, DependenciesRepresenter dr) {
		this.dwellersGraphDesc = dwellersGraphDesc;
		this.dr = dr;
		dwellerVertices = new HashMap<>();
		String relativeTexturesPath = Consts.RELATIVE_TEXTURES_PATH;
		List<String> resourcesNames = dr.getResourcesNames();
		
		for (int i = 0; i < dwellersGraphDesc.length(); i++){
			JSONObject dwellerDesc = (JSONObject)dwellersGraphDesc.get(i);
			Dweller dweller = new Dweller();
			String dwellerName = dwellerDesc.getString(Consts.DWELLER_NAME);
			dweller.setName(dwellerName);
			dweller.setTexturePath(relativeTexturesPath + dwellerDesc.getString(Consts.TEXTURE_PATH));
			HashMap<String, Integer> consumes = new HashMap<>();
			JSONObject consumedResources = dwellerDesc.getJSONObject(Consts.CONSUMES);
			for (String resourceName : resourcesNames){
				consumes.put(resourceName, 0);
			}

			Iterator<?> consumedResourcesKeys = consumedResources.keys();
			while(consumedResourcesKeys.hasNext()){
				String consumedResource = (String) consumedResourcesKeys.next();
				int consumeRate = consumedResources.getInt(consumedResource);
				consumes.put(consumedResource, consumeRate);
			}	
			dweller.setConsumes(consumes);
			String predeccessor = dwellerDesc.getString(Consts.PREDECESSOR);
			String successor = dwellerDesc.getString(Consts.SUCCESSOR);
			dweller.setPredecessor(predeccessor);
			dweller.setSuccessor(successor);
			DwellerNode dwellerNode = new DwellerNode(dweller);
			dwellerVertices.put(dwellerName, dwellerNode);
		}
	}

	
	private JSONArray listToJSONArray(List<Dweller> dwellers){
		JSONArray entities = new JSONArray();
		for(int i = 0; i < dwellers.size(); i++){
			JSONObject entity = new JSONObject()
				.put(Consts.DWELLER_NAME, dwellers.get(i).getName())
				.put(Consts.PREDECESSOR, dwellers.get(i).getPredecessor())
				.put(Consts.SUCCESSOR, dwellers.get(i).getSuccessor());
			entities.put(i, entity);
		}
		return entities;
	}
	

	public void mountDependendenciesGraph() throws CheckException{
		DwellersChecker dwellersChecker = new DwellersChecker(dwellersGraphDesc, dwellerVertices);
		dwellersChecker.check();
		System.out.println("Dwellerts: ");
		mountGraph(dwellerVertices);
		dr.getGraphsHolder().setDwellersGraphs(rootsList);
		dr.getGraphsHolder().setDwellersVertices(dwellerVertices);
	}
	
}
