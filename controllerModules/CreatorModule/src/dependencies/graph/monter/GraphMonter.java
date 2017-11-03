package dependencies.graph.monter;

import graph.GraphNode;
import graph.GraphsHolder;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

class GraphMonter {

	List rootsList;
	
	GraphMonter(){
		rootsList = new ArrayList<>();
	}
	
	void mountGraph(HashMap<String, ? extends GraphNode> vertices){
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
	}
	
}
