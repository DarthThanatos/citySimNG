package mapnode;

import model.DependenciesRepresenter;
import controlnode.Node;
import controlnode.SocketNode;

public class MapNode extends SocketNode{

	public MapNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("Created Map Node");
		nodeName = "MapNode";
	}


	@Override
	public String parseCommand(String command, String[] streamArgs) {
		// TODO Auto-generated method stub
		return null;
	}


}
