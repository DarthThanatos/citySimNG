package mapnode;

import model.DependenciesRepresenter;
import controlnode.Node;
import controlnode.SocketNode;

public class MapNode extends SocketNode{

	public MapNode(Node parent, DependenciesRepresenter dr) {
		super(parent, dr);
		// TODO Auto-generated constructor stub
	}

	@Override
	public void createChildren() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public String parseCommand(String command, String[] streamArgs) {
		// TODO Auto-generated method stub
		return null;
	} 

}
