package corectness.checker;

import entities.Dweller;
import graph.DwellerNode;

import java.util.HashMap;

import graph.ResourceNode;
import model.DependenciesRepresenter;
import org.json.JSONArray;

import constants.Consts;

public class DwellersChecker{

	private LvlMapper lvlMapper;
	private DependenciesRepresenter dr;

	public DwellersChecker(DependenciesRepresenter dr){
		lvlMapper = new LvlMapper();
		this.dr = dr;
	}

	private void checkConsumedResourcesLowerEq(HashMap<String, Integer> resourcesLvls, HashMap<String, Integer> dwellersLvls) throws CheckException {
		for(String dwellerName : dwellersLvls.keySet()){
			Dweller dweller = dr.getGraphsHolder().getDwellerNode(dwellerName).getDweller();
			for (String consumedResource : dweller.getConsumes().keySet()){
				if(dweller.getConsumes().get(consumedResource) == 0) continue;
				if(resourcesLvls.get(consumedResource) > dwellersLvls.get(dwellerName)){
					throw new CheckException("Dweller " + dwellerName + " cannot consume " + consumedResource + " since " + consumedResource + " has bigger lvl");
				}
			}
		}

	}

	public void check() throws CheckException {
		lvlMapper.mapLevels(dr.getGraphsHolder().getResourcesGraphs(), dr.getGraphsHolder().getDwellersGraphs());
		HashMap<String, Integer> dwellersLvls = lvlMapper.getDwellersNodesLevels();
		HashMap<String, Integer> resourcesLvls = lvlMapper.getResourcesNodesLevels();
		checkConsumedResourcesLowerEq(resourcesLvls, dwellersLvls);
	}
}
