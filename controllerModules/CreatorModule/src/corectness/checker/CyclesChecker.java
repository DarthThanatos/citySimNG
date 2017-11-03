package corectness.checker;

import org.jgrapht.alg.CycleDetector;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.json.JSONArray;

import constants.Consts;

public class CyclesChecker implements CorrectnessChecker{

	private JSONArray entities;
	private String key;
	
	
	public CyclesChecker(JSONArray entities, String key) {
		this.key = key;
		this.entities = entities;
	}
	
	@Override
	public void check() throws CheckException{
		  CycleDetector<String, DefaultEdge> cycleDetector;
	      DefaultDirectedGraph<String, DefaultEdge> g;

	      g = new DefaultDirectedGraph<String, DefaultEdge>(DefaultEdge.class);
	      
	      for(int i = 0; i < entities.length(); i++){
	    	  String entityName = entities.getJSONObject(i).getString(key);
	    	  g.addVertex(entityName);
	      }
	      
	      for (int i = 0; i < entities.length(); i++){
	    	  String entityName = entities.getJSONObject(i).getString(key);
	    	  String successorName = entities.getJSONObject(i).getString(Consts.SUCCESSOR);
	    	  String predecessorName = entities.getJSONObject(i).getString(Consts.PREDECESSOR);
	    	  if(!predecessorName.equals("None"))g.addEdge(predecessorName, entityName);
	    	  if(!successorName.equals("None")) g.addEdge(entityName, successorName);
	      }

	      System.out.println(g.toString());

	      // Are there cycles in the dependencies.
	      cycleDetector = new CycleDetector<String, DefaultEdge>(g);
	      // Cycle(s) detected.
	      if (cycleDetector.detectCycles()) throw new CheckException("Cycle detected when considering " + key);
	         
	    	  
	}
}
