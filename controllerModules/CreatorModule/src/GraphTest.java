import  java.io.*;
import java.util.Iterator;
import java.util.Set;

import org.jgrapht.alg.CycleDetector;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.traverse.TopologicalOrderIterator;
import org.json.JSONArray;
import org.json.JSONObject;

import constants.CreatorConsts;


public class GraphTest {
   public static void test(JSONArray entities, String key) {
      CycleDetector<String, DefaultEdge> cycleDetector;
      DefaultDirectedGraph<String, DefaultEdge> g;

      g = new DefaultDirectedGraph<String, DefaultEdge>(DefaultEdge.class);
      
      for(int i = 0; i < entities.length(); i++){
    	  String entityName = entities.getJSONObject(i).getString(key);
    	  g.addVertex(entityName);
      }
      
      for (int i = 0; i < entities.length(); i++){
    	  String entityName = entities.getJSONObject(i).getString(key);
    	  String successorName = entities.getJSONObject(i).getString(CreatorConsts.SUCCESSOR);
    	  String predecessorName = entities.getJSONObject(i).getString(CreatorConsts.PREDECESSOR);
    	  if(!predecessorName.equals("None"))g.addEdge(predecessorName, entityName);
    	  if(!successorName.equals("None")) g.addEdge(entityName, successorName);
      }

      System.out.println(g.toString());

      // Are there cycles in the dependencies.
      cycleDetector = new CycleDetector<String, DefaultEdge>(g);
      // Cycle(s) detected.
      if (cycleDetector.detectCycles()) {
         Iterator<String> iterator;
         Set<String> cycleVertices;
         Set<String> subCycle;
         String cycle;

         System.out.println("Cycles detected.");

         // Get all vertices involved in cycles.
         cycleVertices = cycleDetector.findCycles();

         // Loop through vertices trying to find disjoint cycles.
         while (! cycleVertices.isEmpty()) {
            System.out.println("Cycle:");

            // Get a vertex involved in a cycle.
            iterator = cycleVertices.iterator();
            cycle = iterator.next();

            // Get all vertices involved with this vertex.
            subCycle = cycleDetector.findCyclesContainingVertex(cycle);
            for (String sub : subCycle) {
               System.out.println("   " + sub);
               // Remove vertex so that this cycle is not encountered
               // again.
               cycleVertices.remove(sub);
            }
         }
      }

      // No cycles.  Just output properly ordered vertices.
      else {
         String v;
         TopologicalOrderIterator<String, DefaultEdge> orderIterator;

         orderIterator = new TopologicalOrderIterator<String, DefaultEdge>(g);
         System.out.println("\nOrdering:");
         while (orderIterator.hasNext()) {
            v = orderIterator.next();
            System.out.println(v);
         }
      }
   }
	   
	
	
   public static void dependenciesCycleDetectionTest(){
	   try {
		   System.out.println("Graph test");
		   BufferedReader br = new BufferedReader(new FileReader(new File("..\\..\\resources\\dependencies\\cycle.dep")));
		   String line, dependenciesContent = "";
		   while((line = br.readLine())!= null){
			   dependenciesContent += line + "\n";
		   }
		   JSONObject dependenciesObj = new JSONObject(dependenciesContent);
		   JSONArray resources = DefaultDepTest.retrieveArrayFromObj(dependenciesObj.getJSONObject(CreatorConsts.RESOURCES));
		   JSONArray buildings = DefaultDepTest.retrieveArrayFromObj(dependenciesObj.getJSONObject(CreatorConsts.BUILDINGS));
		   JSONArray dwellers = DefaultDepTest.retrieveArrayFromObj(dependenciesObj.getJSONObject(CreatorConsts.DWELLERS));
		   test(resources, CreatorConsts.RESOURCE_NAME);
		   test(buildings, CreatorConsts.BUILDING_NAME);
		   test(dwellers, CreatorConsts.DWELLER_NAME);
		   br.close();
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	} 
   }
}
