package dependencies.graph.monter;

import corectness.checker.CheckException;
import graph.GraphNode;
import graph.GraphsHolder;
import org.jgrapht.Graph;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

class GraphMonter {

	List rootsList;
	
	GraphMonter(){
		rootsList = new ArrayList<>();
	}
	
	void mountGraph(HashMap<String, ? extends GraphNode> vertices) throws CheckException{
		for (String vertexName: vertices.keySet()){
			GraphNode vertex = vertices.get(vertexName);
			String predeccessorName = vertex.getPredeccessorName();
			if (! predeccessorName.equals("None")){
				GraphNode parent = vertices.get(predeccessorName);
				parent.addChild(vertexName, vertex);
				vertex.setParent(parent);
			}
			else{
				rootsList.add(vertex);
			}
		}
		checkPredSuccConsistency();
	}

	private void checkPredSuccConsistency() throws CheckException{
		for(GraphNode vertex: (List<GraphNode>)rootsList){
			checkSubtreePredSuccConsistency(vertex);
		}
	}

	private void checkSubtreePredSuccConsistency(GraphNode graphNode) throws CheckException{
		if(!graphNode.getSuccessorName().equals("None")) {
			boolean correct = false;
			for (Object childObj : graphNode.getChildren().values()) {
				GraphNode child = (GraphNode)childObj;
				if (child.getName().equals(graphNode.getSuccessorName())){
					correct = true;
				}
			}
			if(!correct) throw new CheckException(
					"Successor of " + graphNode.getName() + " should not be contradicting its Predecessor relationship. Has set "
					+ graphNode.getSuccessorName() + " as the successor, but such was not found amongst entities that pointed at it as their predecessor\n" +
					"(Note: you can fix it by setting the name of the successor of " + graphNode.getName() + " as None or selecting one of the entities which pointed at it as " +
					"their predecessor as its successor)."
			);
		}
		for (Object childObj :  graphNode.getChildren().values()) {
			checkSubtreePredSuccConsistency((GraphNode)childObj);
		}
	}

}
