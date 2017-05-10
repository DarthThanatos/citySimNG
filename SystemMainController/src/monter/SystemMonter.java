package monter;

import java.util.ArrayList;
import java.util.Map;

import controlnode.Node;

public interface SystemMonter {
	
	/*
	 * by the means of this method, all implementing instances of the SystemMonter
	 * interfaces are able to mount the graph of flow control 
	 * @param namesToFill: empty list passed to monter   
	 * returns: the root Node instance, from which control starts to flow (e.g. MainModule)
	 */
	public Node mount(ArrayList<String> namesToFill);
}
