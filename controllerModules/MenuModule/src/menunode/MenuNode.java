package menunode;

import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class MenuNode extends SocketNode{

	private final String EMPTY_JSON_MSG = "{}";
	
	public MenuNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
	}

	public MenuNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
	}
	
	@Override
	public String parseCommand(String command, JSONObject args) {
		if(command.equals("Exit")){
			System.exit(0);
		}
		return EMPTY_JSON_MSG;
	}


	@Override
	public void atStart() {
		
	}


	@Override
	public void atExit() {
		
	}


	@Override
	public void atUnload() {
		
	}


}
