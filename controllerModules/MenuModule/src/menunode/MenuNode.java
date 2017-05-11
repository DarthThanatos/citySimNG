package menunode;

import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class MenuNode extends SocketNode{

	public MenuNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
		System.out.println("menu node created");
	}

	public MenuNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
		System.out.println("menu node created without a dependencies representer's instance");
	}
	@Override
	public String parseCommand(String command, JSONObject args) {
		if(command.equals("Exit")){
			System.out.println("Exiting...");
			System.exit(0);
		}
		return "{}";
	}


	@Override
	public void atStart() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}


	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}


}
