package menunode;

import model.DependenciesRepresenter;
import controlnode.Node;
import controlnode.SocketNode;

public class MenuNode extends SocketNode{

	public MenuNode(DependenciesRepresenter dr) {
		super(dr);
		System.out.println("menu node created");
		nodeName = "MenuNode";
	}


	@Override
	public String parseCommand(String command, String[] streamArgs) {
		if(command.equals("Exit")){
			System.out.println("Exiting...");
			System.exit(0);
		}
		return null;
	}


}
