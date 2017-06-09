package corectness.checker;

import org.json.JSONArray;

public class CyclesChecker extends RedundanciesChecker{

	
	public CyclesChecker(JSONArray entities, String key) {
		super(entities, key);
	}

	class GraphNode{
		
	}
	
	@Override
	public void check() throws CheckException{
		super.check();
	}
}
